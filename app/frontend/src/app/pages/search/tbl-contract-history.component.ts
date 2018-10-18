import { Component, OnInit, Input, OnChanges } from '@angular/core';
import { SearchService } from './search.service';
declare const $: any;
@Component({
  selector: 'discovery-tbl-contract-history',
  templateUrl: './tbl-contract-history.component.html',
  styleUrls: ['./tbl-contract-history.component.css']
})
export class TblContractHistoryComponent implements OnInit, OnChanges {
  @Input()
  duns;
  @Input()
  pools: any[];
  @Input()
  contract_vehicles: any[];
  _contracts: any[];
  contracts_results: any[];
  items_per_page = 50;
  items_total: number;
  num_total_pages: number;
  num_results: number;
  current_page = 1;
  error_message;
  naics: any[] = [];
  naic_code = 'All';
  piid = 'All';
  next: number;
  prev: number;
  enable_paging = false;
  history_no_results = false;
  spinner = false;
  ordering = '';
  params: string;
  interval;

  constructor(private searchService: SearchService) {}

  ngOnInit() {
    this.initNaicsList();
  }

  ngOnChanges() {
    if (this.duns && this.duns !== '') {
      this.getContracts(
        this.duns,
        this.current_page,
        this.piid,
        this.naic_code,
        this.ordering
      );
    }
  }
  get contracts() {
    return this._contracts;
  }
  set contracts(contracts) {
    this._contracts = contracts;
  }
  getContracts(
    duns: string,
    page: number,
    piid: string,
    naic: string,
    ordering: string
  ) {
    let page_path = '';
    if (page > 1) {
      page_path = '&page=' + page;
    }
    this.current_page = page;
    this.enable_paging = false;
    this.history_no_results = false;
    this.initScrollBars();
    this.spinner = true;
    this.resetTableScrolling();
    this.searchService
      .getVendorContractHistory(duns, page_path, piid, naic, ordering)
      .subscribe(
        data => {
          this.contracts = data;
          this.contracts_results = data['results'];
          this.items_total = data['count'];
          this.num_results = data['results'].length;
          this.num_total_pages = Math.floor(
            (this.items_total + this.items_per_page - 1) / this.items_per_page
          );
          this.setPreviousNext();
          this.enable_paging = true;
          this.spinner = false;
          if (this.num_results === 0) {
            this.history_no_results = true;
          }
        },
        error => (this.error_message = <any>error)
      );
  }
  resetTableScrolling() {
    if (document.getElementById('tbl-contract-history')) {
      /** Reset scroll window widths on re submit */
      $(
        '#overflow-contract-history .scroll-div1, #overflow-contract-history .scroll-div2'
      ).css('width', '100%');
    }
  }
  initScrollBars() {
    this.resetTableScrolling();
    this.interval = setInterval(() => {
      if (document.getElementById('tbl-contract-history')) {
        /** Reset scroll window widths on re submit */
        const w =
          document.getElementById('tbl-contract-history').offsetWidth + 'px';
        $(
          '#overflow-contract-history .scroll-div1, #overflow-contract-history .scroll-div2'
        ).css('width', w);
        if (
          $('#scroll-view').css('width') ===
          $('#tbl-contract-history').css('width')
        ) {
          $(
            '#overflow-contract-history .scroll-div1, #overflow-contract-history .scroll-div2'
          ).css('width', '100%');
        }
        $('.scroll-view-topscroll').scroll(function() {
          $('.scroll-view').scrollLeft(
            $('.scroll-view-topscroll').scrollLeft()
          );
        });
        $('.scroll-view').scroll(function() {
          $('.scroll-view-topscroll').scrollLeft(
            $('.scroll-view').scrollLeft()
          );
        });
        clearInterval(this.interval);
      }
    }, 500);
  }
  orderBy(ordering: any[]) {
    const order_by = ordering['sort'] + ordering['ordering'];
    this.ordering = ordering['ordering'];
    this.getContracts(this.duns, 1, this.piid, this.naic_code, order_by);
  }
  getVehicleDescription(vehicle: string) {
    return this.searchService.getItemDescription(
      this.contract_vehicles,
      vehicle,
      'id',
      'name'
    );
  }
  initNaicsList() {
    this.searchService.getNaics(['All']).subscribe(
      data => {
        this.naics = this.buildNaicsItems(data['results']);
        this.naics.sort(this.searchService.sortByCodeAsc);
      },
      error => (this.error_message = <any>error)
    );
  }
  buildNaicsItems(obj: any[]) {
    const naics = [];
    for (const pool of obj) {
      for (const naic of pool.naics) {
        const item = {};
        item['code'] = naic.code;
        item['description'] = naic.description;
        if (!this.searchService.existsIn(naics, naic.code, 'code')) {
          naics.push(item);
        }
      }
    }
    return naics;
  }
  setPreviousNext() {
    if (this.contracts['next'] !== null) {
      const str = this.contracts['next'];
      if (str.indexOf('&page=') !== -1) {
        const arr_next = str.split('&page=');
        this.next = +arr_next[1];
      }
    }
    if (this.contracts['previous'] !== null) {
      const str = this.contracts['previous'];
      if (str.indexOf('&page=') !== -1) {
        const arr_prev = str.split('&page=');
        this.prev = +arr_prev[1];
      } else {
        this.prev = 1;
      }
    }
  }
  prevPage() {
    this.getContracts(
      this.duns,
      this.prev,
      this.piid,
      this.naic_code,
      this.ordering
    );
  }
  nextPage() {
    this.getContracts(
      this.duns,
      this.next,
      this.piid,
      this.naic_code,
      this.ordering
    );
  }
  getRowNum(n: number) {
    return (
      n + this.current_page * this.items_per_page - (this.items_per_page - 1)
    );
  }
  getViewingItems(): string {
    const start = this.getRowNum(this.current_page) - this.current_page;
    const end = start + this.num_results - 1;
    return start + ' - ' + end;
  }
  filterByContracts(contracts: any[]) {
    const items: any[] = [];
    for (const item of contracts) {
      for (const prop of this.contracts_results) {
        if (prop['base_piid'] === item) {
          items.push(prop);
        }
      }
    }
    return items;
  }
  setParams() {
    let params = '';
    if (this.naic_code !== 'All') {
      params += 'naics=' + this.naic_code;
    } else {
      params = '';
    }
    if (this.piid !== 'All') {
      if (params !== '') {
        params += '&';
      }
      params += 'memberships=' + this.piid;
    }
    this.params = params;
  }
  onChangeNaic() {
    this.getContracts(this.duns, 1, this.piid, this.naic_code, this.ordering);
    this.setParams();
  }
  onChangeMembership() {
    this.getContracts(this.duns, 1, this.piid, this.naic_code, this.ordering);
    this.setParams();
  }
}
