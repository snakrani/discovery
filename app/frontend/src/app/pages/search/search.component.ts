import { Component, OnInit, Input, ViewChild } from '@angular/core';
import { SearchService } from './search.service';
import { Router, ActivatedRoute } from '@angular/router';
import { ActiveFiltersComponent } from './filters/active-filters.component';
import { ModalService } from '../../common/modal.service';
import { FiltersComponent } from './filters.component';
@Component({
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css']
})
export class SearchComponent implements OnInit {
  @Input()
  selected_filters: any[];
  @ViewChild(ActiveFiltersComponent)
  activeFiltersComponent: ActiveFiltersComponent;
  @ViewChild(FiltersComponent)
  filtersComponent: FiltersComponent;

  vw_contracts = true;
  vw_vendors = false;
  error_message;
  contracts_compare;
  contracts_results = [];
  contracts_w_no_records = [];
  vendors_results;
  vendors_no_results = false;
  show_details = false;
  show_results = false;
  sbd_col = false;
  _spinner: boolean;
  set_asides;
  vehicles_selected;
  vehicles_radios;
  compare_tbl;
  vehicles;
  results;
  filtered_results;
  _sort_by: string;
  num_show = 3;
  spinner = false;

  constructor(
    private searchService: SearchService,
    private router: Router,
    private route: ActivatedRoute,
    private modalService: ModalService
  ) {}

  ngOnInit() {
    /** Check to see if there are any queryparams */
    if (this.route.snapshot.queryParamMap.keys.length > 0) {
      this.spinner = true;
    }
  }
  get sort_by(): string {
    return this._sort_by;
  }
  set sort_by(value: string) {
    this._sort_by = value;
    this.filtered_results = this.sort_by
      ? this.filterResultsByVehicle(this.sort_by)
      : this.results;
  }

  buildSelectedItems(arr: string[]): any[] {
    const items = [];
    for (const i of arr) {
      const item = {};
      item['value'] = i;
      items.push(item);
    }
    return items;
  }

  submitSelectedFilters(filters) {
    this.spinner = true;
    this.searchService.activeFilters = filters;
    this.searchService.setQueryParams(filters);

    this.searchService.getVendors(this.searchService.activeFilters).subscribe(
      data => {
        if (data['count'] === 0) {
          this.spinner = false;
          this.vendors_no_results = true;
          this.show_results = true;
          this.results = [];
          this.filtered_results = [];
          return;
        }
        this.results = this.buildVendorByVehicle(data['results']);
        this.filtered_results = this.results;
        this.vendors_no_results = false;
        this.show_results = true;
        this.spinner = false;
        this.buildContractCompare();
        this.sort_by = this.getFirstVehicleWithVendors();
        this.viewContracts();
      },
      error => (this.error_message = <any>error)
    );
  }
  getFirstVehicleWithVendors() {
    for (const item of this.compare_tbl) {
      if (item.vendors_results_total > 0) {
        return item.id;
      }
    }
  }
  /** Checks if vehicles were submitted  */
  returnSubmittedVehicles(): any[] {
    for (const item of this.searchService.activeFilters) {
      if (item.name === 'vehicles') {
        return item;
      }
    }
    return [];
  }
  filterResultsByVehicle(vehicle: string) {
    return this.results.vendors.filter(
      vendor => vendor.vehicles.indexOf(vehicle) !== -1
    );
  }
  showVendorDetails(vendor: number) {
    this.show_details = true;
  }
  clearActiveFilters(bool) {
    this.activeFiltersComponent.clear();
  }
  viewVendors() {
    this.vw_vendors = true;
    this.vw_contracts = false;
  }
  viewContracts() {
    this.vw_contracts = true;
    this.vw_vendors = false;
  }
  buildVendorByVehicle(obj: any[]) {
    const vehicles_submitted = this.returnSubmittedVehicles();
    const results = {};
    results['vehicles'] = [];
    const vehicles: any[] = [];
    for (const item of obj) {
      const vendor = {};
      const asides_arr = [];
      vendor['name'] = item.name;
      vendor['duns'] = item.duns;
      vendor['contracts'] = item.number_of_contracts;
      vendor['vehicles'] = this.returnVehicleVendors(item.pools);

      if (vehicles_submitted['selected']) {
        results['vehicles'] = this.returnVehicleValues(
          vehicles_submitted['selected']
        );
      } else {
        for (const i of item.pools) {
          if (!results['vehicles'].includes(i.pool.vehicle.id)) {
            results['vehicles'].push(i.pool.vehicle.id);
          }
        }
      }

      if (item.pools[0].setasides) {
        for (const asides of item.pools[0].setasides) {
          asides_arr.push(asides['code']);
        }
        vendor['setasides'] = asides_arr;
      } else {
        vendor['setasides'] = [];
      }
      vehicles.push(vendor);
    }
    results['vendors'] = vehicles;
    // console.log(results);
    return results;
  }
  returnVehicleValues(obj: any[]) {
    const arr: any[] = [];
    for (const i of obj) {
      arr.push(i['value']);
    }
    return arr.sort(this.searchService.sortByNameAsc);
  }
  returnVehicleVendors(obj: any[]) {
    const vendors = [];
    for (const item of obj) {
      if (!vendors.includes(item.pool.vehicle.id)) {
        vendors.push(item.pool.vehicle.id);
      }
    }
    return vendors;
  }
  countVendorsByVehicle(vehicle: string) {
    const count = this.results.vendors.filter(
      item => item.vehicles.indexOf(vehicle) !== -1
    );
    return count.length;
  }
  buildContractCompare() {
    const compare: any[] = [];
    this.contracts_w_no_records = [];
    for (const vehicle of this.results.vehicles) {
      const item: any[] = [];
      item['id'] = vehicle;
      item['vendors_total'] = 0;
      item['vendors_results_total'] = this.countVendorsByVehicle(vehicle);
      item['description'] = this.filtersComponent.getVehicleDescription(
        vehicle
      );
      item[
        'service_categories'
      ] = this.filtersComponent.getServiceCategoriesByVehicle(vehicle);
      item['capabilities'] = 0;
      item['naics'] = this.filtersComponent.getNaicsByVehicle(vehicle);
      item['pscs'] = [];
      item['tier'] = '';
      item['gsa'] = '';
      item['website'] = '';
      item['ordering_guide'] = '';
      compare.push(item);
      if (item['vendors_results_total'] === 0) {
        this.contracts_w_no_records.push({ name: item['description'] });
      }
    }
    this.compare_tbl = compare;
  }
  viewVehicleVendors(vehicle: string) {
    this.sort_by = vehicle;
    this.viewVendors();
  }
  exists(value: string, key: string, arr: any[]): boolean {
    for (const i of arr) {
      if (i[key] === value) {
        return true;
      }
    }
    return false;
  }

  commaSeparatedList(obj: any[], key: string) {
    let items = '';
    for (const i of obj) {
      items += i[key] + ', ';
    }
    return items.slice(0, -2);
  }
  openModal(id: string) {
    this.modalService.open(id);
  }
  toggleSBD() {
    this.sbd_col = !this.sbd_col;
  }
  closeModal(id: string) {
    this.modalService.close(id);
  }
  returnSetAside(arr: any[], code: string): boolean {
    if (arr.length > 0) {
      return arr.includes(code);
    } else {
      return false;
    }
  }
}
