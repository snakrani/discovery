import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { SearchService } from '../search.service';
import { ActivatedRoute } from '@angular/router';
declare let document: any;

@Component({
  selector: 'discovery-filter-contract-threshold',
  templateUrl: './filter-contract-threshold.component.html',
  styles: []
})
export class FilterContractThresholdComponent implements OnInit {
  min = 0;
  max = 10000000;
  items = [
    { description: 'All', id: '0', checked: true },
    { description: '$0 - $250K', id: '0-250000', checked: false },
    { description: '$250K - $1M', id: '250001-1000000', checked: false },
    { description: '$1M - $5M', id: '1000001-5000000', checked: false },
    { description: '$5M - $10M', id: '5000001-10000000', checked: false },
    { description: '$10M - $100M', id: '10000001-100000000', checked: false },
    { description: '$100M+', id: '100000001-1000000000', checked: false }
  ];
  item_selected: any[] = [];
  @Input()
  opened = false;
  @Output()
  emmitSelected: EventEmitter<number> = new EventEmitter();
  @Output()
  emmitLoaded: EventEmitter<string> = new EventEmitter();
  name = 'Vendor Contract Value History';
  queryName = 'threshold';
  id = 'filter-threshold';
  error_message;
  count = 0;
  _threshold = '0';
  value_set = false;

  /** Generate inputs labels & values
   *  with these
   */
  json_value = 'id';
  json_description = 'description';
  constructor(
    private searchService: SearchService,
    private route: ActivatedRoute
  ) {}

  ngOnInit() {
    /** Grab the queryparams and sets default values
     *  on inputs Ex. checked, selected, keywords, etc */
    if (this.route.snapshot.queryParamMap.has(this.queryName)) {
      const values: string[] = this.route.snapshot.queryParamMap
        .get(this.queryName)
        .split('__');
      for (let i = 0; i < this.items.length; i++) {
        if (values[0] === this.items[i][this.json_value]) {
          this.items[i]['checked'] = true;
          this.threshold = values[0];
        }
      }
      /** Open accordion */
      this.opened = true;
    } else {
      this.opened = false;
    }
    this.emmitLoaded.emit(this.queryName);
  }
  get threshold(): string {
    return this._threshold;
  }
  set threshold(value: string) {
    this._threshold = value;
    if (!this.value_set) {
      /** Only emit this once */
      this.emmitSelected.emit(1);
      this.value_set = true;
    }
  }
  getSelected(): any[] {
    const item = [];
    if (this.threshold !== '0') {
      item['name'] = this.queryName;
      item['description'] = this.name;
      item['items'] = [{ value: this.threshold }];
    }
    return item;
  }
  reset() {
    /** Set default values */
    this.threshold = '0';
  }
}
