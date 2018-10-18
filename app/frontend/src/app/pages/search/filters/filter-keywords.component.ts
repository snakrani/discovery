import {
  Component,
  OnInit,
  Input,
  Output,
  EventEmitter,
  ViewChild,
  AfterContentInit
} from '@angular/core';
import { SearchService } from '../search.service';
import { ActivatedRoute, Router } from '@angular/router';
import { FilterSelectedComponent } from './filter-selected.component';
declare let autocomplete: any;
declare let document: any;
declare const $: any;
@Component({
  selector: 'discovery-filter-keywords',
  templateUrl: './filter-keywords.component.html',
  styles: []
})
export class FilterKeywordsComponent implements OnInit, AfterContentInit {
  @ViewChild(FilterSelectedComponent)
  msgAddedItem: FilterSelectedComponent;
  items: any[] = [];
  keywords_results: any[] = [];
  _keywords = '';
  items_selected: any[] = [];
  @Input()
  opened = true;
  @Output()
  emmitSelected: EventEmitter<number> = new EventEmitter();
  @Output()
  emmitLoaded: EventEmitter<string> = new EventEmitter();
  name = 'Keywords';
  queryName = 'keywords';
  id = 'filter-keywords';
  placeholder;
  error_message;
  json_value = 'id';
  json_description = 'name';
  constructor(
    private searchService: SearchService,
    private route: ActivatedRoute,
    private router: Router
  ) {}
  set keywords(value: string) {
    this._keywords = value;
  }
  get keywords(): string {
    return this._keywords;
  }
  ngOnInit() {}
  ngAfterContentInit() {
    this.setKeywordsList();
  }

  setKeywordsList() {
    this.placeholder = 'Loading keywords...';

    this.searchService.getKeywords().subscribe(data => {
      this.items = data['results'];
      this.searchService.keywords = data['results'];
      this.keywords_results = this.searchService.buildKeywordsDropdown(
        this.items
      );
      // this.searchService.setKeywordAutoComplete(
      //   this.keywords_results,
      //   this.id
      // );
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
      this.emmitLoaded.emit(this.queryName);
      this.placeholder = 'Enter keywords...';
    });
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
        if (+this.items[i][this.json_value] === id) {
          return this.items[i][this.json_description];
        }
      }
    }
  }
  addKeywords(code) {
    if (!this.searchService.existsIn(this.items_selected, code, 'value')) {
      this.addItem(code);
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
  removeItem(value: string) {
    for (let i = 0; i < this.items_selected.length; i++) {
      if (this.items_selected[i]['value'] === value) {
        this.items_selected.splice(i, 1);
      }
    }
    this.emmitSelected.emit(0);
  }
}
