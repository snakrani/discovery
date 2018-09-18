import { Component, OnInit, Input, OnChanges } from '@angular/core';
import { SearchService } from './search.service';

@Component({
  selector: 'discovery-tbl-contract-history',
  templateUrl: './tbl-contract-history.component.html',
  styleUrls: ['./tbl-contract-history.component.css']
})
export class TblContractHistoryComponent implements OnInit, OnChanges {
  @Input()
  duns;
  contracts: any[];
  contracts_results: any[];
  items_per_page = 50;
  items_total: number;
  error_message;
  page = 0;
  next = 0;
  prev = 0;
  constructor(private searchService: SearchService) {}

  ngOnInit() {}
  ngOnChanges() {
    if (this.duns) {
      this.getContracts(this.duns, this.page);
    }
  }
  getContracts(duns: string, page: number) {
    let page_path = '';
    if (page > 0) {
      page_path = '&page=' + page;
    }
    this.searchService.getContracts(duns, page_path).subscribe(
      data => {
        this.contracts = data;
        this.contracts_results = data['results'];
        this.items_total = data['count'];
        console.log(this.contracts);
        this.setPreviousNext();
      },
      error => (this.error_message = <any>error)
    );
  }
  setPreviousNext() {
    if (this.contracts['next'] !== null) {
      const str = this.contracts['next'];
      if (str.indexOf('&page=') !== -1) {
        const arr_next = str.split('&page=');
        this.next = arr_next[1];
      }
    } else {
      this.next = 0;
    }
    if (this.contracts['previous'] !== null) {
      const str = this.contracts['previous'];
      if (str.indexOf('&page=') !== -1) {
        const arr_prev = str.split('&page=');
        this.prev = arr_prev[1];
      } else {
        this.prev = 0;
      }
    }
  }
  prevPage() {
    console.log(this.prev);
    this.getContracts(this.duns, this.prev);
  }
  nextPage() {
    console.log(this.next);
    this.getContracts(this.duns, this.next);
  }
  buildPaging() {}
  getViewingItems(): string {
    let items = '';
    if (this.prev === 0) {
      items = '1 - ' + this.items_per_page;
    } else {
      const page_items = this.items_per_page * this.next;
      items = '' + page_items;
    }
    return items;
  }
}
