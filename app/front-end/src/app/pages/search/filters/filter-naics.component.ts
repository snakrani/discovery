import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { SearchService } from '../search.service';
import { ActivatedRoute, Router } from '@angular/router';
declare let autocomplete: any;
declare let document: any;
declare let $: any;
@Component({
  selector: 'discovery-filter-naics',
  templateUrl: './filter-naics.component.html',
  styles: []
})
export class FilterNaicsComponent implements OnInit {
  @Input()
  items: any[];
  items_filtered: any[] = [];
  items_selected: any[] = [];
  @Input()
  opened = true;
  @Output()
  emmitSelected: EventEmitter<number> = new EventEmitter();
  @Output()
  emmitLoaded: EventEmitter<number> = new EventEmitter();
  @Output()
  emmitNaics: EventEmitter<any> = new EventEmitter();
  name = 'NAICs';
  queryName = 'naics';
  id = 'filter-naics';
  placeholder;
  error_message;
  filtered_naics;
  naic = '0';
  ln;
  /** Sample json
  {

  };
  */

  json_value = 'code';
  json_description = 'description';
  constructor(
    private searchService: SearchService,
    private route: ActivatedRoute,
    private router: Router
  ) {}
  ngOnInit() {
    this.initNaicsList(['All']);
  }

  initNaicsList(vehicles) {
    this.searchService.getNaics(vehicles).subscribe(
      data => {
        this.items = this.buildItems(data['results']);
        this.items.sort(sortByCodeAsc);
        this.setFilteredItems(vehicles);

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
          // this.opened = false;
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
        this.emmitLoaded.emit(1);
        this.emmitNaics.emit(this.items_filtered);
      },
      error => (this.error_message = <any>error)
    );
  }
  setFilteredItems(vehicles) {
    this.items_filtered =
      vehicles[0] !== 'All' ? this.filterByVehicles(vehicles) : this.items;
    this.items_filtered.sort(sortByCodeAsc);
    this.ln = this.items_filtered.length;
    /** Remove all selected items
     *  that are not within filtered list
     */
    for (const item of this.items_selected) {
      if (!this.existsIn(this.items_filtered, item['value'], 'id')) {
        this.removeItem(item['value']);
        this.naic = '0';
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
  getNaicsByVehicle(vehicle: string): any[] {
    let items: any[] = [];
    const abr = vehicle.substr(0, 3);
    items = this.items.filter(naics => naics.vehicle_id.indexOf(abr) !== -1);
    return items;
  }
  buildItems(obj: any[]) {
    const naics = [];
    for (const pool of obj) {
      for (const naic of pool.naics) {
        const item = {};
        item['code'] = naic.code;
        item['description'] = naic.description;
        item['vehicle_id'] = pool.vehicle.id;
        if (!this.existsIn(naics, naic.code, 'code')) {
          naics.push(item);
        }
      }
    }
    return naics;
  }
  buildItemsByVehicle(obj: any[]) {
    const naics = [];
    for (const pool of obj) {
      const item = {};
      item['vehicle_id'] = pool.vehicle.id;
      item['naics'] = this.setNaics(pool.naics);
      if (!this.existsIn(naics, naics['vehicle_id'], 'vehicle_id')) {
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
      if (!this.existsIn(items, i.code, 'code')) {
        items.push(item);
      }
    }
    return items;
  }
  addNaic() {
    if (!this.exists(this.naic) && this.naic !== '0') {
      this.addItem(this.naic);
    }
  }
  existsIn(obj: any[], value: string, key: string): boolean {
    for (let i = 0; i < obj.length; i++) {
      if (obj[i][key] === value) {
        return true;
      }
    }
    return false;
  }
  exists(value: string): boolean {
    for (let i = 0; i < this.items_selected.length; i++) {
      if (this.items_selected[i][this.json_value] === value) {
        return true;
      }
    }
    return false;
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
    this.naic = '0';
    this.items_selected = [];
  }
  getItemDescription(value: string): string {
    if (value) {
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
function sortByCodeAsc(i1, i2) {
  if (i1.code > i2.code) {
    return 1;
  } else if (i1.code === i2.code) {
    return 0;
  } else {
    return -1;
  }
}
