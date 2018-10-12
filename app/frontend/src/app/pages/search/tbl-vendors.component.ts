import {
  Component,
  OnInit,
  Input,
  OnChanges,
  Output,
  EventEmitter
} from '@angular/core';
import { SearchService } from './search.service';
declare const window: any;
@Component({
  selector: 'discovery-tbl-vendors',
  templateUrl: './tbl-vendors.component.html',
  styleUrls: ['./tbl-vendors.component.css']
})
export class TblVendorsComponent implements OnInit, OnChanges {
  @Input()
  vehicle = '';
  @Input()
  obligated_amounts_list: any[] = [];
  @Input()
  agency_performance_list: any[] = [];
  @Input()
  total_vendors: number;
  @Output()
  emitActivateSpinner: EventEmitter<boolean> = new EventEmitter();
  @Output()
  emitVehicle: EventEmitter<string> = new EventEmitter();
  @Output()
  emitDuns: EventEmitter<string> = new EventEmitter();
  sbd_col = false;
  items_per_page = 50;
  items_total: number;
  num_total_pages: number;
  num_results: number;
  current_page = 1;
  set_asides;
  vehicles_selected;
  vehicles_radios;
  vehicles;
  results;
  vendors;
  error_message;
  next: number;
  prev: number;
  enable_paging = false;
  vendors_results;
  vendors_no_results = false;
  show_results = false;
  contracts_w_no_records;
  filters;
  loading = true;

  constructor(private searchService: SearchService) {}

  ngOnInit() {}
  ngOnChanges() {
    if (this.vehicle) {
      this.filters = this.setOnlyVehicleSelected(this.vehicle);
      this.getVendors(this.current_page);
    }
  }
  showSpinner(bool: boolean) {
    setTimeout(() => {
      this.emitActivateSpinner.emit(bool);
    });
  }
  setOnlyVehicleSelected(vehicle: string) {
    const filters = [];
    for (const filter of this.searchService.activeFilters) {
      if (filter.name === 'vehicles') {
        const item = {};
        item['description'] = 'Contract Vehicles';
        item['name'] = 'vehicles';
        item['selected'] = [{ value: vehicle }];
        filters.push(item);
      } else {
        filters.push(filter);
      }
    }
    return filters;
  }
  getVendors(page) {
    this.loading = true;
    this.showSpinner(true);
    let page_path = '';
    if (page > 1) {
      page_path = '&page=' + page;
    }
    this.current_page = +page;
    this.enable_paging = false;
    this.searchService.getVendors(this.filters, page_path).subscribe(
      data => {
        if (this.total_vendors === 0) {
          this.loading = false;
          this.vendors_no_results = true;
          this.show_results = true;
          this.enable_paging = false;
          this.results = [];
          this.vendors = [];
          return;
        }
        this.items_total = this.total_vendors;
        this.num_results = data['results'].length;
        this.num_total_pages = Math.floor(
          (this.items_total + this.items_per_page - 1) / this.items_per_page
        );

        this.items_total = this.total_vendors;
        this.results = data;
        this.vendors = this.buildVendorByVehicle(data['results']);

        this.vendors_no_results = false;
        this.show_results = true;
        this.loading = false;
        this.showSpinner(false);
        this.setPreviousNext();
        this.enable_paging = true;
        window.scroll({
          top: 90,
          left: 0,
          behavior: 'smooth'
        });
      },
      error => (this.error_message = <any>error)
    );
  }

  setPreviousNext() {
    if (this.results['next'] !== null) {
      const str = this.results['next'];
      this.next = this.searchService.getPageNumber(str);
    }
    if (this.results['previous'] !== null) {
      const str = this.results['previous'];
      if (str.indexOf('&page=') !== -1) {
        this.next = this.searchService.getPageNumber(str);
      } else {
        this.prev = 1;
      }
    }
  }
  showVendorDetails(duns: string) {
    this.emitDuns.emit(duns);
  }
  prevPage() {
    this.getVendors(this.prev);
  }
  nextPage() {
    this.getVendors(this.next);
  }
  getRowNum(n: number) {
    return (
      n + this.current_page * this.items_per_page - (this.items_per_page - 1)
    );
  }
  filterResultsByVehicle(vehicle: string) {
    return this.results.vendors.filter(
      vendor => vendor.vehicles.indexOf(vehicle) !== -1
    );
  }
  toggleSBD() {
    this.sbd_col = !this.sbd_col;
  }
  /** Checks if vehicles were submitted  */
  returnSubmittedVehicles(): any[] {
    for (const item of this.filters) {
      if (item.name === 'vehicles') {
        return item;
      }
    }
    return [];
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

      if (
        this.obligated_amounts_list.length > 0 &&
        this.searchService.existsIn(this.obligated_amounts_list, item.duns, '')
      ) {
        vehicles.push(vendor);
      } else if (this.obligated_amounts_list.length === 0) {
        vehicles.push(vendor);
      }
    }
    results['vendors'] = vehicles;
    return results;
  }
  countVendorsByVehicle(vehicle: string) {
    const count = this.results.vendors.filter(
      item => item.vehicles.indexOf(vehicle) !== -1
    );
    return count.length;
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
  getViewingItems(): string {
    const start = this.getRowNum(this.current_page) - this.current_page;
    const end = start + this.num_results - 1;
    return start + ' - ' + end;
  }
  returnSetAside(arr: any[], code: string): boolean {
    if (arr.length > 0) {
      return arr.includes(code);
    } else {
      return false;
    }
  }
}
