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
declare let document: any;
declare let autocomplete: any;
@Component({
  selector: 'discovery-filter-psc',
  templateUrl: './filter-psc.component.html',
  styles: []
})
export class FilterPscComponent implements OnInit, OnChanges {
  @ViewChild(FilterSelectedComponent)
  msgAddedItem: FilterSelectedComponent;
  @Input()
  items: any[];
  items_filtered: any[] = [];
  items_selected: any[] = [];
  @Input()
  opened = false;
  @Output()
  emmitSelected: EventEmitter<number> = new EventEmitter();
  @Output()
  emmitLoaded: EventEmitter<string> = new EventEmitter();
  @Output()
  emmitPSCs: EventEmitter<any> = new EventEmitter();
  name = 'PSCs';
  queryName = 'pscs';
  id = 'filter-pscs';
  placeholder;
  error_message;
  filtered_naics;
  psc = '0';
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
  ngOnInit() {}
  ngOnChanges() {
    if (this.items.length > 1) {
      this.buildItems(this.items);
    }
  }
  setFilteredItems(vehicles) {
    this.items_filtered =
      vehicles[0] !== 'All' ? this.filterByVehicles(vehicles) : this.items;
    this.items_filtered.sort(this.searchService.sortByCodeAsc);
    /** Remove all selected items
     *  that are not within filtered list
     */
    for (const item of this.items_selected) {
      if (
        !this.searchService.existsIn(this.items_filtered, item['value'], 'id')
      ) {
        this.psc = '0';
      }
    }
  }
  filterByVehicles(vehicles: any[]) {
    const items: any[] = [];
    for (const item of vehicles) {
      for (const prop of this.items) {
        const arr = item.split('_');
        if (prop['vehicle_id'].indexOf(arr[0]) !== -1) {
          if (!this.searchService.existsIn(items, prop.code, 'code')) {
            items.push(prop);
          }
        }
      }
    }
    return items;
  }
  getPSCsByVehicle(vehicle: string): any[] {
    let items: any[] = [];
    const abr = vehicle.substr(0, 3);
    items = this.items.filter(pscs => pscs.vehicle_id.indexOf(abr) !== -1);
    return items;
  }
  buildItems(obj: any[]) {
    const pscs = [];
    for (const pool of obj) {
      for (const psc of pool.psc) {
        const item = {};
        item['code'] = psc.code;
        item['description'] = psc.description;
        item['vehicle_id'] = pool.vehicle.id;
        if (!this.searchService.existsIn(pscs, psc.code, 'code')) {
          pscs.push(item);
        }
      }
    }
    this.items = pscs;
    this.items.sort(this.searchService.sortByCodeAsc);
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
  buildItemsByVehicle(obj: any[]) {
    const pscs = [];
    for (const pool of obj) {
      const item = {};
      item['vehicle_id'] = pool.vehicle.id;
      item['pscs'] = this.setPSCs(pool.psc);
      if (
        !this.searchService.existsIn(pscs, pscs['vehicle_id'], 'vehicle_id')
      ) {
        pscs.push(item);
      }
    }
    return pscs;
  }
  setPSCs(obj: any[]) {
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
  addPSC() {
    if (!this.exists(this.psc) && this.psc !== '0') {
      this.addItem(this.psc);
    }
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
    this.psc = '0';
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
    this.msgAddedItem.showMsg();
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
