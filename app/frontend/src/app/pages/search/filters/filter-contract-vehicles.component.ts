import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { SearchService } from '../search.service';
import { ActivatedRoute } from '@angular/router';
declare let document: any;
@Component({
  selector: 'discovery-filter-contract-vehicles',
  templateUrl: './filter-contract-vehicles.component.html'
})
export class FilterContractVehiclesComponent implements OnInit {
  @Input()
  sharedFiltersLoaded = false;
  @Input()
  items: any[] = [];
  _items_selected: any[] = [];
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
  /** Sample json
  {
    id: "BMO_SB",
    name: "BMO Small Business",
    small_business: true,
    numeric_pool: true,
    display_number:
    false
  };
  */
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

  loaded() {
    this.emmitLoaded.emit(this.queryName);
  }
  getSelected(): any[] {
    const item = [];
    if (this._items_selected.length > 0) {
      item['name'] = this.queryName;
      item['description'] = this.name;
      item['items'] = this._items_selected;
    }
    return item;
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
