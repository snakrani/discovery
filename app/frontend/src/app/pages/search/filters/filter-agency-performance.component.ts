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
  selector: 'discovery-filter-agency-performance',
  templateUrl: './filter-agency-performance.component.html',
  styles: []
})
export class FilterAgencyPerformanceComponent implements OnInit, OnChanges {
  @ViewChild(FilterSelectedComponent)
  msgAddedItem: FilterSelectedComponent;
  items: any[] = [];
  items_selected: any[] = [];
  @Input()
  opened = false;
  @Output()
  emmitSelected: EventEmitter<number> = new EventEmitter();
  @Output()
  emmitLoaded: EventEmitter<string> = new EventEmitter();
  name = 'Agency Performance History';
  queryName = 'agency_performance';
  id = 'filter-agency-performance';
  error_message;
  agency = '0';
  duns_list: any[] = [];
  /** Sample json
  {

  };
  */
  /** Generate inputs labels & values
   *  with these
   */
  json_value = 'code';
  json_description = 'description';
  constructor(
    private searchService: SearchService,
    private route: ActivatedRoute
  ) {}

  ngOnInit() {
    this.searchService.getAgencyPerformanceNames().subscribe(
      data => {
        this.items = data['results'];

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
        this.emmitLoaded.emit(this.queryName);
      },
      error => {
        this.error_message = <any>error;
      }
    );
  }
  ngOnChanges() {
    // if (this.items.length > 1) {
    //   this.buildItems(this.items);
    //   this.emmitLoaded.emit(this.queryName);
    // }
  }

  buildItems(obj: any[]) {
    const agency = [];
    for (const vehicle of obj) {
      const item = {};
      item['code'] = vehicle.tier.number.toString();
      item['description'] = vehicle.tier.name;
      item['vehicle_id'] = vehicle.id;
      if (!this.searchService.existsIn(agency, item['code'], 'code')) {
        agency.push(item);
      }
    }
    this.items = agency;
    this.items.sort(this.searchService.sortByDescriptionAsc);

    this.emmitLoaded.emit(this.queryName);
  }
  getAgencyPerformanceDuns() {
    this.duns_list = [];
    // Set agency IDs
    const ids = '';
    this.searchService.getAgencyPerformanceDuns(ids).subscribe(
      data => {
        this.duns_list = data['results'];
      },
      error => (this.error_message = <any>error)
    );
  }
  getDunsList(): any[] {
    let list = [];
    if (this.items_selected.length > 0) {
      list = this.duns_list;
    }
    return list;
  }
  exists(value: string): boolean {
    for (let i = 0; i < this.items_selected.length; i++) {
      if (this.items_selected[i]['value'] === value) {
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
    this.items_selected = [];
    for (let i = 0; i < this.items.length; ++i) {
      document.getElementById(
        this.id + '-' + this.items[i][this.json_value]
      ).checked = false;
    }
  }
  addAgency() {
    if (!this.exists(this.agency) && this.agency !== '0') {
      this.addItem(this.agency);
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
