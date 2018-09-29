import {
  Component,
  OnInit,
  Output,
  EventEmitter,
  Input,
  ViewChild
} from '@angular/core';
import { SearchService } from './search.service';
import { FilterContractVehiclesComponent } from './filters/filter-contract-vehicles.component';
import { FilterSbdComponent } from './filters/filter-sbd.component';
import { ActivatedRoute, Router } from '@angular/router';
import { FilterKeywordsComponent } from './filters/filter-keywords.component';
import { FilterNaicsComponent } from './filters/filter-naics.component';
import { FilterServiceCategoriesComponent } from './filters/filter-service-categories.component';
import { FilterCertificationsComponent } from './filters/filter-certifications.component';
import { FilterContractPricingTypeComponent } from './filters/filter-contract-pricing-type.component';
import { FilterContractThresholdComponent } from './filters/filter-contract-threshold.component';
import { FilterAgencyPerformanceComponent } from './filters/filter-agency-performance.component';
import { FilterPscComponent } from './filters/filter-psc.component';
import { FilterZoneComponent } from './filters/filter-zone.component';

@Component({
  selector: 'discovery-filters',
  templateUrl: './filters.component.html',
  styleUrls: ['./filters.component.css']
})
export class FiltersComponent implements OnInit {
  /** START Define filter components */
  @ViewChild(FilterContractVehiclesComponent)
  filterContractVehiclesComponent: FilterContractVehiclesComponent;
  @ViewChild(FilterSbdComponent)
  filterSbdComponent: FilterSbdComponent;
  @ViewChild(FilterKeywordsComponent)
  filterKeywordsComponent: FilterKeywordsComponent;
  @ViewChild(FilterNaicsComponent)
  filterNaicsComponent: FilterNaicsComponent;
  @ViewChild(FilterServiceCategoriesComponent)
  filterServiceCategories: FilterServiceCategoriesComponent;
  @ViewChild(FilterCertificationsComponent)
  filterCertifications: FilterCertificationsComponent;
  @ViewChild(FilterContractPricingTypeComponent)
  filterContractPricing: FilterContractPricingTypeComponent;
  @ViewChild(FilterContractThresholdComponent)
  filterContractThreshold: FilterContractThresholdComponent;
  @ViewChild(FilterAgencyPerformanceComponent)
  filterAgencyPerformance: FilterAgencyPerformanceComponent;
  @ViewChild(FilterPscComponent)
  filterPscComponent: FilterPscComponent;
  @ViewChild(FilterZoneComponent)
  filterZoneComponent: FilterZoneComponent;
  filters_list: any[];
  /** END Define filter components */
  @Input()
  parentSpinner: boolean;
  @Output()
  emmitFilters: EventEmitter<any> = new EventEmitter();
  @Output()
  emmitResetFilters: EventEmitter<any> = new EventEmitter();
  @Output()
  emitHideFilters: EventEmitter<number> = new EventEmitter();
  APP_ASSETS = '';
  disabled_btn = true;
  num_items_selected = 0;
  loaded_filters: any[] = [];
  error_message;
  filters_submitted: any[];
  params_submitted = false;
  sharedFiltersLoaded = false;
  vehicles: any[] = [];
  pools: any[] = [];
  spinner = true;

  constructor(
    private searchService: SearchService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit() {
    /** Set the filters that are going to be used */
    this.filters_list = [
      this.filterKeywordsComponent,
      this.filterContractVehiclesComponent,
      this.filterSbdComponent,
      this.filterServiceCategories,
      this.filterNaicsComponent,
      this.filterPscComponent,
      this.filterZoneComponent
    ];
    /**
     *
      this.filterZoneComponent
      this.filterCertifications,
      this.filterContractPricing,
      this.filterContractThreshold,
      this.filterAgencyPerformance
       */
    this.initPools(['All']);
  }
  initVehicles() {
    this.searchService.getContractVehicles().subscribe(
      data => {
        this.vehicles = data['results'];
        const queryName = 'vehicles';
        /** Grab the queryparams and sets default values
         *  on inputs Ex. checked, selected, keywords, etc */
        if (this.route.snapshot.queryParamMap.has(queryName)) {
          const values: string[] = this.route.snapshot.queryParamMap
            .get(queryName)
            .split('__');
          for (let i = 0; i < this.vehicles.length; i++) {
            if (values.includes(this.vehicles[i]['id'])) {
              this.vehicles[i]['checked'] = true;
              this.filterContractVehiclesComponent.addItem(
                this.vehicles[i]['id'],
                this.vehicles[i]['name']
              );
            }
          }
          /** Open accordion */
          this.filterContractVehiclesComponent.opened = true;
        }
        this.spinner = false;
        this.filterContractVehiclesComponent.loaded();
      },
      error => (this.error_message = <any>error)
    );
  }
  initPools(vehicles) {
    this.searchService.getPools(vehicles).subscribe(
      data => {
        this.pools = data['results'];
        this.initVehicles();
      },
      error => (this.error_message = <any>error)
    );
  }
  resetFilters() {
    this.num_items_selected = 0;
    this.disabled_btn = true;
    for (let i = 0; i < this.filters_list.length; i++) {
      if (this.filters_list[i]) {
        this.filters_list[i].reset();
      }
    }
  }
  activateSubmit(n: number): void {
    if (n === 1) {
      this.num_items_selected++;
    } else {
      this.num_items_selected--;
    }
    if (this.num_items_selected > 0) {
      this.disabled_btn = false;
    } else {
      this.disabled_btn = true;
    }
  }
  getSelectedFilters() {
    const filters: any[] = [];
    for (let i = 0; i < this.filters_list.length; i++) {
      if (this.filters_list[i]) {
        const filter_items = this.filters_list[i].getSelected();
        if (filter_items['name']) {
          const item = {
            name: filter_items['name'],
            description: filter_items['description'],
            selected: filter_items['items']
          };
          filters.push(item);
        }
      }
    }
    return filters;
  }
  emmitSelectedFilters() {
    this.params_submitted = true;
    const filters: any[] = this.getSelectedFilters();
    this.emmitFilters.emit(filters);
    this.hideFilters();
  }
  filterOthersByVehicles(vehicles: any[]) {
    let arr = [];
    if (vehicles[0] === 'All') {
      arr = vehicles;
    } else {
      for (const i of vehicles) {
        arr.push(i.value);
      }
    }
    this.filterServiceCategories.setFilteredItems(arr);
    this.filterNaicsComponent.setFilteredItems(arr);
    this.filterPscComponent.setFilteredItems(arr);
  }
  getServiceCategoriesByVehicle(vehicle: string) {
    const obj: any[] = this.filterServiceCategories.getServiceCategoriesByVehicle(
      vehicle
    );
    return obj;
  }
  getVehicleDescription(vehicle: string) {
    const desc = this.filterContractVehiclesComponent.getItemDescription(
      vehicle
    );
    return desc;
  }
  getNaicsByVehicle(vehicle: string) {
    const obj: any[] = this.filterNaicsComponent.getNaicsByVehicle(vehicle);
    return obj;
  }
  getPSCsByVehicle(vehicle: string) {
    const obj: any[] = this.filterPscComponent.getPSCsByVehicle(vehicle);
    return obj;
  }
  getSetAsides() {
    const setasides = this.filterSbdComponent.getItems();
    return setasides;
  }
  getSelectedVehicles(): any[] {
    const vehicles: any[] = this.filterContractVehiclesComponent.getSelected();
    return vehicles;
  }
  getVehicleData(vehicle: string) {
    const obj = this.filterContractVehiclesComponent.getVehicleInfo(vehicle);
    return obj;
  }
  getResults(filter: string) {
    if (!this.searchService.existsIn(this.loaded_filters, filter, 'name')) {
      const item = {};
      item['name'] = filter;
      this.loaded_filters.push(item);
    }

    /** Filters need to be loaded before
     *  displaying compare table.
     */

    if (this.loaded_filters.length === this.filters_list.length) {
      if (
        this.num_items_selected > 0 &&
        this.route.snapshot.queryParamMap.keys.length > 0 &&
        !this.params_submitted
      ) {
        this.emmitSelectedFilters();
      }
    }
  }
  hideFilters() {
    this.emitHideFilters.emit(1);
  }
}
