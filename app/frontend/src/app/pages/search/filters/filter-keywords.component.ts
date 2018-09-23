import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { SearchService } from '../search.service';
import { ActivatedRoute, Router } from '@angular/router';
declare let autocomplete: any;
declare let document: any;
@Component({
  selector: 'discovery-filter-keywords',
  templateUrl: './filter-keywords.component.html',
  styles: []
})
export class FilterKeywordsComponent implements OnInit {
  items: any[] = [];
  keywords_results: any[] = [];
  _keywords = '';
  items_selected: any[] = [];
  @Input()
  opened = false;
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
  ngOnInit() {
    this.setKeywordsList();
  }
  setKeywordsList() {
    this.placeholder = 'Loading keywords...';
    this.searchService.getKeywords().subscribe(data => {
      this.items = data['results'];
      this.keywords_results = this.buildKeywordsDropdown(this.items);
      this.placeholder = 'Enter keywords...';
      autocomplete(
        document.getElementById('keywords-input'),
        this.keywords_results
      );

      /** Grab the queryparams and sets default values
       *  on inputs Ex. checked, selected, keywords, etc */
      if (this.route.snapshot.queryParamMap.has(this.queryName)) {
        const values: string[] = this.route.snapshot.queryParamMap
          .get(this.queryName)
          .split('__');

        for (const id of values) {
          const desc = this.getItemDescription(+id);
          this.addItem(id, desc);
        }
        /** Open accordion */
        this.opened = true;
      } else {
        this.opened = false;
      }
      this.emmitLoaded.emit(this.queryName);
    });
  }
  buildKeywordsDropdown(obj: any[]): any[] {
    const keywords = [];
    for (const item of obj) {
      keywords.push(item['name']);
    }
    return keywords;
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
        if (this.items[i][this.json_value] === id) {
          return this.items[i][this.json_description];
        }
      }
    }
  }
  addKeywords() {
    this.keywords = document.getElementById('keywords-input').value;
    if (!this.exists(this.keywords)) {
      this.addItem('', this.keywords);
    }
    this.keywords = '';
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
  }
  addItem(id: string, desc: string) {
    const item = {};
    if (id && id !== '') {
      item['value'] = id;
    } else {
      item['value'] = this.getItemId(desc);
    }
    item['description'] = desc;

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
