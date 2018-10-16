import {
  Component,
  OnInit,
  Input,
  Output,
  EventEmitter,
  ViewChild,
  OnChanges
} from '@angular/core';
import { SearchService } from '../search.service';
import { ActivatedRoute } from '@angular/router';
import { FilterSelectedComponent } from './filter-selected.component';
declare let document: any;
@Component({
  selector: 'discovery-filter-contract-vehicles',
  templateUrl: './filter-contract-vehicles.component.html'
})
export class FilterContractVehiclesComponent implements OnInit, OnChanges {
  @ViewChild(FilterSelectedComponent)
  msgAddedItem: FilterSelectedComponent;
  @Input()
  sharedFiltersLoaded = false;
  @Input()
  items: any[] = [];
  _items_selected: any[] = [];
  all_vehicles: any[] = [];
  @Input()
  opened = false;
  @Output()
  emmitSelected: EventEmitter<number> = new EventEmitter();
  @Output()
  emmitLoaded: EventEmitter<string> = new EventEmitter();
  @Output()
  emmitItem: EventEmitter<any> = new EventEmitter();
  name = 'Contract Vehicles';
  queryName = 'vehicles';
  id = 'filter-vehicles';
  error_message;

  /** Generate inputs labels & values
   *  with these
   */
  json_value = 'id';
  json_description = 'name';
  constructor(
    private searchService: SearchService,
    private route: ActivatedRoute
  ) {}

  ngOnInit() {}
  ngOnChanges() {
    if (this.items && this.items.length > 0) {
      this.setAllVehicles();
    }
  }
  loaded() {
    this.emmitLoaded.emit(this.queryName);
  }
  setAllVehicles() {
    for (const i of this.items) {
      const item = {};
      item['description'] = i.name;
      item['value'] = i.id;
      this.all_vehicles.push(item);
    }
  }
  getAllVehicles() {
    return this.all_vehicles;
  }
  getSelected(): any[] {
    const item = [];
    if (this._items_selected.length > 0) {
      item['name'] = this.queryName;
      item['description'] = this.name;
      item['items'] = this._items_selected;
    } else {
      item['name'] = this.queryName;
      item['description'] = this.name;
      item['items'] = this.all_vehicles;
    }
    return item;
  }
  getItems() {
    return this.items;
  }

  getVehicleInfo(vehicle: string): any[] {
    for (const item of this.items) {
      if (item['id'] === vehicle) {
        return item;
      }
    }
    return [];
  }
  reset() {
    this._items_selected = [];
    for (let i = 0; i < this.items.length; ++i) {
      document.getElementById(
        this.id + '-' + this.items[i][this.json_value]
      ).checked = false;
    }
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
  addItem(key: string, title: string) {
    const item = {};
    item['description'] = title;
    item['value'] = key;
    this._items_selected.push(item);
    this.emmitSelected.emit(1);
    this.msgAddedItem.showMsg();
  }
  removeItem(key: string) {
    for (let i = 0; i < this._items_selected.length; i++) {
      if (this._items_selected[i]['value'] === key) {
        this._items_selected.splice(i, 1);
      }
    }
    this.emmitSelected.emit(0);
  }
  onChange(key: string, title: string, isChecked: boolean) {
    if (isChecked) {
      this.addItem(key, title);
    } else {
      this.removeItem(key);
    }

    if (this._items_selected.length === 0) {
      /** If none are selected, get All */
      this.emmitItem.emit(['All']);
    } else {
      this.emmitItem.emit(this._items_selected);
    }
  }
}
