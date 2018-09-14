import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { SearchService } from '../search.service';
import { ActivatedRoute } from '@angular/router';
declare let document: any;
@Component({
  selector: 'discovery-filter-sbd',
  templateUrl: './filter-sbd.component.html'
})
export class FilterSbdComponent implements OnInit {
  @Input()
  items: any[] = [];
  items_selected: any[] = [];
  @Input()
  opened = false;
  @Output()
  emmitSelected: EventEmitter<number> = new EventEmitter();
  @Output()
  emmitLoaded: EventEmitter<number> = new EventEmitter();
  name = 'Type of Set Asides';
  queryName = 'setasides';
  id = 'filter-sbd';
  error_message;

  /** Sample json
  {
    count: 8,
    next: null,
    previous: null,
    results: [
      {
        code: 'A6',
        name: '8(A)',
        description: '8(A)',
        far_order: 1,
        url: 'http://localhost:8080/api/setasides/A6'
      }
    ]
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
    this.setInputItems();
  }
  setInputItems() {
    this.searchService.getSetAsides().subscribe(
      data => {
        this.items = data['results'];
        this.emmitLoaded.emit(1);
        /** Grab the queryparams and sets default values
         *  on inputs Ex. checked, selected, keywords, etc */
        if (this.route.snapshot.queryParamMap.has(this.queryName)) {
          const values: string[] = this.route.snapshot.queryParamMap
            .get(this.queryName)
            .split('__');
          for (let i = 0; i < this.items.length; i++) {
            if (values.includes(this.items[i][this.json_value])) {
              this.items[i]['checked'] = true;
              this.addItem(
                this.items[i][this.json_value],
                this.items[i][this.json_description]
              );
            }
          }
          /** Open accordion */
          this.opened = true;
        } else {
          this.opened = false;
        }
      },
      error => (this.error_message = <any>error)
    );
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
  getItems() {
    return this.items;
  }
  reset() {
    this.items_selected = [];
    for (let i = 0; i < this.items.length; ++i) {
      document.getElementById(
        this.id + '-' + this.items[i][this.json_value]
      ).checked = false;
    }
  }
  addItem(key: string, title: string) {
    const item = {};
    item['description'] = title;
    item['value'] = key;
    this.items_selected.push(item);
    this.emmitSelected.emit(1);
  }
  removeItem(key: string) {
    for (let i = 0; i < this.items_selected.length; i++) {
      if (this.items_selected[i]['value'] === key) {
        this.items_selected.splice(i, 1);
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
  }
}
