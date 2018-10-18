import {
  Component,
  OnInit,
  Input,
  Output,
  EventEmitter,
  OnChanges,
  ViewChild
} from '@angular/core';
import { SearchService } from '../search.service';
import { ActivatedRoute } from '@angular/router';
import { FilterSelectedComponent } from './filter-selected.component';
declare let document: any;
@Component({
  selector: 'discovery-filter-service-categories',
  templateUrl: './filter-service-categories.component.html',
  styles: []
})
export class FilterServiceCategoriesComponent implements OnInit, OnChanges {
  @ViewChild(FilterSelectedComponent)
  msgAddedItem: FilterSelectedComponent;
  @Input()
  items: any[] = [];
  items_filtered: any[];
  items_selected: any[] = [];
  @Input()
  opened = false;
  @Output()
  emmitSelected: EventEmitter<number> = new EventEmitter();
  @Output()
  emmitLoaded: EventEmitter<string> = new EventEmitter();
  name = 'Service Categories';
  queryName = 'service_categories';
  id = 'filter-service-cat';
  error_message;
  category = '0';
  sortBy = 'vehicle';
  ascending = true;

  /** Generate inputs labels & values
   *  with these
   */
  json_value = 'id';
  json_description = 'name';
  constructor(
    private searchService: SearchService,
    private route: ActivatedRoute
  ) {}

  ngOnInit() {
    // this.initServiceCategories(['All']);
  }
  ngOnChanges() {
    if (this.items.length > 1) {
      this.buildItems(this.items);
    }
  }
  initServiceCategories(vehicles) {
    this.searchService.getPools(vehicles).subscribe(
      data => {
        this.buildItems(data['results']);
        /** Grab the queryparams and sets default values
         *  on inputs Ex. checked, selected, keywords, etc */
        if (this.route.snapshot.queryParamMap.has(this.queryName)) {
          const values: string[] = this.route.snapshot.queryParamMap
            .get(this.queryName)
            .split('__');

          for (const item of values) {
            this.addItem(item);
          }

          /** Open accordion */
          this.opened = true;
        } else {
          this.opened = false;
        }
        /** Check if there are selected vehicles
         *  and sort dropdown based on vehicle id
         */
        if (this.route.snapshot.queryParamMap.has('vehicles')) {
          const values: string[] = this.route.snapshot.queryParamMap
            .get('vehicles')
            .split('__');

          this.setFilteredItems(values);
        }

        this.emmitLoaded.emit(this.queryName);
      },
      error => (this.error_message = <any>error)
    );
  }
  loaded() {
    this.emmitLoaded.emit(this.queryName);
  }
  setFilteredItems(vehicles) {
    this.items_filtered =
      vehicles[0] !== 'All' ? this.filterByVehicles(vehicles) : this.items;
    this.items_filtered.sort(this.searchService.sortByVehicleAsc);
    /** Remove all selected items
     *  that are not within filtered list
     */
    for (const item of this.items_selected) {
      if (
        !this.searchService.existsIn(this.items_filtered, item['value'], 'id')
      ) {
        this.category = '0';
      }
    }
  }
  filterByVehicles(vehicles: any[]) {
    const items: any[] = [];
    for (const item of vehicles) {
      for (const prop of this.items) {
        if (prop['vehicle_id'] === item) {
          items.push(prop);
        }
      }
    }
    return items;
  }
  getItems() {
    return this.items;
  }
  getServiceCategoriesByVehicle(vehicle: string): any[] {
    const items: any[] = [];
    for (const item of this.items) {
      if (item['vehicle_id'] === vehicle) {
        items.push(item);
      }
    }
    return items.sort(this.searchService.sortByVehicleAsc);
  }
  buildItems(obj: any[]) {
    const categories = [];
    for (const category of obj) {
      const item = {};
      item['id'] = category['id'];
      item['name'] = category['name'];
      item['vehicle_id'] = category['vehicle']['id'];
      item['vehicle'] = category['vehicle']['id'].replace('_', ' ');
      categories.push(item);
    }
    this.items = categories;
    this.items_filtered = this.items;

    /** Grab the queryparams and sets default values
     *  on inputs Ex. checked, selected, keywords, etc */
    if (this.route.snapshot.queryParamMap.has(this.queryName)) {
      const values: string[] = this.route.snapshot.queryParamMap
        .get(this.queryName)
        .split('__');

      for (const item of values) {
        this.addItem(item);
      }

      /** Open accordion */
      this.opened = true;
    } else {
      this.opened = false;
    }
    /** Check if there are selected vehicles
     *  and sort dropdown based on vehicle id
     */
    if (this.route.snapshot.queryParamMap.has('vehicles')) {
      const values: string[] = this.route.snapshot.queryParamMap
        .get('vehicles')
        .split('__');

      this.setFilteredItems(values);
    } else {
      this.setFilteredItems(['All']);
    }

    this.emmitLoaded.emit(this.queryName);
  }
  addCategory() {
    if (
      !this.searchService.existsIn(
        this.items_selected,
        this.category,
        'value'
      ) &&
      this.category !== '0'
    ) {
      this.addItem(this.category);
    }
  }
  getSelected(): any[] {
    const item = [];
    if (this.items_selected.length > 0) {
      item['name'] = this.queryName;
      item['description'] = this.name;
      item['items'] = this.items_selected;
    }
    return item;
  }
  reset() {
    this.items_selected = [];
    this.category = '0';
  }
  getItemDescription(value: string): string {
    if (this.items) {
      for (let i = 0; i < this.items.length; i++) {
        if (this.items[i][this.json_value] === value) {
          return this.items[i][this.json_description];
        }
      }
    }
  }
  addItem(value: string) {
    const item = {};
    item['value'] = value;
    item['description'] = this.getItemDescription(value);
    this.items_selected.push(item);
    this.emmitSelected.emit(1);
    this.msgAddedItem.showMsg();
  }
  removeItem(key: string) {
    for (let i = 0; i < this.items_selected.length; i++) {
      if (this.items_selected[i]['value'] === key) {
        this.items_selected.splice(i, 1);
      }
    }
    this.emmitSelected.emit(0);
  }
}
