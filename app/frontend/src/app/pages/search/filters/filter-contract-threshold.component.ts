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
    { description: 'All', id: '10000000', checked: true },
    { description: '$0 - $500K', id: '0-500000', checked: false },
    { description: '$500K - $1M', id: '500001-1000000', checked: false },
    { description: '$1M - $5M', id: '1000001-5000000', checked: false },
    { description: '$5M - $10M', id: '5000001-10000000', checked: false }
  ];
  item_selected = { description: '', value: '' };
  @Input()
  opened = false;
  @Output()
  emmitSelected: EventEmitter<number> = new EventEmitter();
  @Output()
  emmitLoaded: EventEmitter<number> = new EventEmitter();
  name = 'Vendor Contract Value History';
  queryName = 'threshold';
  id = 'filter-threshold';
  error_message;
  count = 0;

  /** Sample json
 {
  "results": [
    { "description": "All", "id": "10000000" },
    { "description": "$0 - $500K", "id": "0-500000" },
    { "description": "$500K - $1M", "id": "500001-1000000" },
    { "description": "$1M - $5M", "id": "1000001-5000000" },
    { "description": "$5M - $10M", "id": "5000001-10000000" }
  ]
  }
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
          this.setValue(
            this.items[i][this.json_value].toString(),
            this.items[i][this.json_description]
          );
        }
      }
      /** Open accordion */
      this.opened = true;
      console.log('open ' + this.id);
    } else {
      this.opened = false;
    }
  }
  // setInputItems() {
  //   this.searchService.getContractValueHistory().subscribe(
  //     data => {
  //       this.items = data['results'];
  //       this.emmitLoaded.emit(1);
  //       /** Grab the queryparams and sets default values
  //        *  on inputs Ex. checked, selected, keywords, etc */
  //       if (this.route.snapshot.queryParamMap.has(this.queryName)) {
  //         const values: string[] = this.route.snapshot.queryParamMap
  //           .get(this.queryName)
  //           .split('__');
  //         for (let i = 0; i < this.items.length; i++) {
  //           if (values[0] === this.items[i][this.json_value]) {
  //             this.items[i]['checked'] = true;
  //             this.setValue(
  //               this.items[i][this.json_value].toString(),
  //               this.items[i][this.json_description]
  //             );
  //           }
  //         }
  //         /** Open accordion */
  //         this.opened = true;
  //         console.log('open ' + this.id);
  //       } else {
  //         this.opened = false;
  //       }
  //     },
  //     error => (this.error_message = <any>error)
  //   );
  // }
  getSelected(): any[] {
    const item = [];
    const value = this.item_selected.value;
    if (value !== '' && value !== this.max.toString()) {
      // ** Build obj only if is not default value */
      item['name'] = this.queryName;
      item['description'] = this.name;
      item['items'] = [this.item_selected];
    }
    return item;
  }
  reset() {
    /** Set default values */
    this.item_selected.value = this.max.toString();
    this.item_selected.description = 'All';
    for (let i = 0; i < this.items.length; ++i) {
      document.getElementById(this.id + '-' + i).checked = false;
    }
    document.getElementById(this.id + '-0').checked = true;
  }
  setValue(value: string, title: string) {
    this.item_selected.description = title;
    this.item_selected.value = value;
  }
  onChange(value: string, description: string, isChecked: boolean) {
    if (isChecked) {
      this.setValue(value, description);
      if (this.count === 0) {
        this.emmitSelected.emit(1);
      }
      // if (description === 'All') {
      //   this.emmitSelected.emit(0);
      // }
    }
  }
}
