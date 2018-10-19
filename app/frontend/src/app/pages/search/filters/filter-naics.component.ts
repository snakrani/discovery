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
import { ActivatedRoute, Router } from '@angular/router';
import { FilterSelectedComponent } from './filter-selected.component';
declare let autocomplete: any;
declare let document: any;
declare let $: any;
@Component({
  selector: 'discovery-filter-naics',
  templateUrl: './filter-naics.component.html',
  styles: []
})
export class FilterNaicsComponent implements OnInit, OnChanges {
  @ViewChild(FilterSelectedComponent)
  msgAddedItem: FilterSelectedComponent;
  @Input()
  items: any[] = [];
  items_filtered: any[] = [];
  items_selected: any[] = [];
  keywords_results: any[] = [];
  @Input()
  opened = false;
  @Output()
  emmitSelected: EventEmitter<number> = new EventEmitter();
  @Output()
  emmitLoaded: EventEmitter<string> = new EventEmitter();
  @Output()
  emmitNaics: EventEmitter<any> = new EventEmitter();
  name = 'NAICs';
  queryName = 'naics';
  id = 'filter-naics';

  placeholder;
  error_message;
  filtered_naics;
  naics;
  ln;

  json_value = 'code';
  json_description = 'description';
  constructor(
    private searchService: SearchService,
    private route: ActivatedRoute,
    private router: Router
  ) {}
  ngOnInit() {}
  ngOnChanges() {
    if (this.items.length > 1) {
      this.setKeywordsList();
    }
  }
  setKeywordsList() {
    this.items = this.buildNaicsItems(this.items);
    /** Grab the queryparams and sets default values
     *  on inputs Ex. checked, selected, keywords, etc */
    if (this.route.snapshot.queryParamMap.has(this.queryName)) {
      const values: string[] = this.route.snapshot.queryParamMap
        .get(this.queryName)
        .split('__');

      for (const id of values) {
        this.addItem(id);
      }
      /** Open accordion */
      this.opened = true;
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

    this.placeholder = 'Enter NAIC or keywords...';
    this.emmitLoaded.emit(this.queryName);
  }
  setFilteredItems(vehicles) {
    this.items_filtered =
      vehicles[0] !== 'All'
        ? this.filterByVehicles(vehicles)
        : this.returnUnique(this.items);
    this.items_filtered.sort(this.searchService.sortById);
    this.keywords_results = this.items_filtered;
  }
  returnUnique(items: any[]): any[] {
    const unique_items = [];
    for (const item of items) {
      if (!this.searchService.existsIn(unique_items, item.id, 'id')) {
        unique_items.push(item);
      }
    }
    return unique_items;
  }
  buildNaicsItems(obj: any[]): any[] {
    const naics = [];
    for (const pool of obj) {
      for (const naic of pool.naics) {
        const item = {};
        item['id'] = naic.code;
        item['text'] = naic.code + ' - ' + naic.description;
        item['vehicle_id'] = pool.vehicle.id;
        naics.push(item);
      }
    }
    naics.sort(this.searchService.sortById);
    return naics;
  }

  getItemId(value: string): string {
    if (value) {
      for (let i = 0; i < this.items.length; i++) {
        if (this.items[i][this.json_description] === value) {
          return this.items[i][this.json_value];
        }
      }
    }
  }
  getItemDescription(id: number): string {
    if (id) {
      for (let i = 0; i < this.items.length; i++) {
        if (+this.items[i]['id'] === id) {
          return this.items[i]['text'];
        }
      }
    }
  }
  addKeywords(code) {
    if (code === '0') {
      this.reset();
      return;
    }
    if (
      !this.searchService.existsIn(this.items_selected, code, 'value') &&
      this.searchService.existsIn(this.items_filtered, code, 'id')
    ) {
      this.addItem(code);
    }
  }
  addItem(id: string) {
    const item = {};
    if (id && id !== '') {
      item['value'] = id;
      item['description'] = this.getItemDescription(+id);
    }
    this.items_selected.push(item);
    this.emmitSelected.emit(1);
    this.msgAddedItem.showMsg();
  }
  filterByVehicles(vehicles: any[]) {
    const items: any[] = [];
    for (const item of vehicles) {
      for (const prop of this.items) {
        const arr = item.split('_');
        if (prop['vehicle_id'].indexOf(arr[0]) !== -1) {
          if (!this.searchService.existsIn(items, prop.id, 'id')) {
            items.push(prop);
          }
        }
      }
    }
    return items;
  }
  getNaicsByVehicle(vehicle: string): any[] {
    // console.log(vehicle);
    let items: any[] = [];
    const abr = vehicle.substr(0, 3);
    const unique_items = this.filterByVehicles([vehicle]);
    items = unique_items.filter(naics => naics.vehicle_id !== -1);
    return items;
  }

  buildItemsByVehicle(obj: any[]) {
    const naics = [];
    for (const pool of obj) {
      const item = {};
      item['vehicle_id'] = pool.vehicle.id;
      item['naics'] = this.setNaics(pool.naics);
      if (
        !this.searchService.existsIn(naics, naics['vehicle_id'], 'vehicle_id')
      ) {
        naics.push(item);
      }
    }
    return naics;
  }
  setNaics(obj: any[]) {
    const items: any[] = [];
    for (const i of obj) {
      const item = {};
      item['code'] = i.code;
      item['description'] = i.description;
      if (!this.searchService.existsIn(items, i.code, 'code')) {
        items.push(item);
      }
    }
    return items;
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
  }
  removeItem(value: string) {
    for (let i = 0; i < this.items_selected.length; i++) {
      if (this.items_selected[i]['value'] === value) {
        this.items_selected.splice(i, 1);
      }
    }
    this.emmitSelected.emit(0);
  }
}
