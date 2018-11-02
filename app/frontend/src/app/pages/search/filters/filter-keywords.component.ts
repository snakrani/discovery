import {
  Component,
  OnInit,
  Input,
  Output,
  EventEmitter,
  ViewChild,
  AfterContentInit,
  OnChanges
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
export class FilterKeywordsComponent
  implements OnInit, OnChanges, AfterContentInit {
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
  @Output()
  emitClearedSelected: EventEmitter<boolean> = new EventEmitter();
  name = 'Keywords';
  queryName = 'keywords';
  id = 'filter-keywords';
  placeholder;
  error_message;
  json_value = 'id';
  json_description = 'name';
  timer: any;
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
    if (this.searchService.keywords && this.searchService.keywords.length > 0) {
      const items = this.searchService.buildKeywordsDropdown(
        this.searchService.keywords
      );
      this.emmitLoaded.emit(this.queryName);
      this.timer = setTimeout(() => {
        this.keywords_results = items;
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

        clearTimeout(this.timer);
      }, 300);
    } else {
      this.setKeywordsList();
    }
  }
  ngOnChanges() {}

  setKeywordsList() {
    this.searchService.getKeywords().subscribe(data => {
      this.items = data['results'];
      this.searchService.keywords = data['results'];
      this.keywords_results = this.searchService.buildKeywordsDropdown(
        this.items
      );

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
    });
  }
  getItemId(value: string): string {
    if (value) {
      for (let i = 0; i < this.items.length; i++) {
        if (this.items[i]['id'] === value) {
          return this.items[i]['text'];
        }
      }
    }
  }
  getItemDescription(id: number): string {
    if (id) {
      for (let i = 0; i < this.keywords_results.length; i++) {
        if (+this.keywords_results[i]['id'] === id) {
          return this.keywords_results[i]['text'];
        }
      }
    }
  }
  addKeywords(code) {
    if (code === '0') {
      this.reset();
      return;
    }
    if (!this.searchService.existsIn(this.items_selected, code, 'value')) {
      this.addItem(code);
    }
  }
  getSelected(selectedOnly: boolean): any[] {
    const item = [];
    if (selectedOnly) {
      return this.items_selected;
    }
    if (this.items_selected.length > 0) {
      item['name'] = this.queryName;
      item['description'] = this.name;
      item['items'] = this.items_selected;
    }
    return item;
  }
  reset() {
    this.items_selected = [];
    this.emitClearedSelected.emit(true);
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
    if (this.items_selected.length === 0) {
      this.emitClearedSelected.emit(true);
    }
    this.emmitSelected.emit(0);
  }
}
