import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { SearchService } from '../search.service';
import { ActivatedRoute } from '@angular/router';
declare let document: any;
declare let autocomplete: any;
@Component({
  selector: 'discovery-filter-psc',
  templateUrl: './filter-psc.component.html',
  styles: []
})
export class FilterPscComponent implements OnInit {
  @Input()
  items: any[] = [];
  items_w_codes: any[] = [];
  items_selected: any[] = [];
  @Input()
  opened = false;
  @Output()
  emmitSelected: EventEmitter<number> = new EventEmitter();
  @Output()
  emmitLoaded: EventEmitter<number> = new EventEmitter();
  @Output()
  emmitNaics: EventEmitter<number> = new EventEmitter();
  name = 'PSCs';
  queryName = 'psc_performance';
  id = 'filter-psc-performance';
  error_message;
  psc;
  /** Sample json
  {

  };
  */
  /** Generate inputs labels & values
   *  with these
   */
  json_value = 'id';
  json_description = 'description';
  constructor(
    private searchService: SearchService,
    private route: ActivatedRoute
  ) {}

  ngOnInit() {}
  // setInputItems() {
  //   // Stop observable
  //   this.searchService.getPSCs(this.psc).subscribe(
  //     data => {
  //       this.items = this.buildList(data['results']);
  //       autocomplete(document.getElementById('pscs-input'), this.items);
  //     },
  //     error => (this.error_message = <any>error)
  //   );
  // }
  getPSCsbyNAICs(naics) {
    this.searchService.getPSCsByNAICs(naics).subscribe(
      data => {
        // this.items = this.buildList(data['results']);
        this.items = data['results'];
        console.log(data['results']);
        this.emmitLoaded.emit(1);
        // this.items_w_codes = data['results'];
        // autocomplete(document.getElementById('pscs-input'), this.items);
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
      },
      error => (this.error_message = <any>error)
    );
  }
  searchTerm(term: string) {
    if (term !== '') {
      this.searchService.getPSCsByTerm(term).subscribe(
        data => {
          // this.items = this.buildList(data['results']);
          this.items = data['results'];
          console.log(data['results']);
          this.emmitLoaded.emit(1);
          // this.items_w_codes = data['results'];
          // autocomplete(document.getElementById('pscs-input'), this.items);
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
        },
        error => (this.error_message = <any>error)
      );
    }
  }
  addPSC() {
    const value = document.getElementById('pscs-input').value;
    if (!this.exists(value) && value !== '0') {
      this.addItem(value);
    }
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
  buildList(arr): any[] {
    const results: any[] = [];
    for (const ele of arr) {
      if (ele['description']) {
        results.push(ele['description']);
      }
    }
    return results;
  }
  reset() {
    this.items_selected = [];
    this.psc = '0';
  }
  getItemCode(term: string): string {
    for (let i = 0; i < this.items_w_codes.length; i++) {
      if (this.items_w_codes[i]['description'] === term) {
        return this.items_w_codes[i]['code'];
      }
    }
  }
  addItem(value: string) {
    console.log(value);
    const item = {};
    item['value'] = this.getItemCode(value);
    item['description'] = value;
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
}
