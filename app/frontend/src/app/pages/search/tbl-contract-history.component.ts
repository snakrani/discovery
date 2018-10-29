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
  error_message;
  current_page = 1;
  naics: any[] = [];
  naic_code = 'All';
  piid = 'All';
  countries: any[];
  states: any[];
  country = '0';
  state = '0';
  params: string;
  next: number;
  prev: number;
  enable_paging = false;
  history_no_results = false;
  spinner = false;
  ordering = '';
  interval;

  constructor(private searchService: SearchService) {}

  ngOnInit() {
    this.initNaicsList();
  }

  ngOnChanges() {
    this.current_page = 1;
    this.naic_code = 'All';
    this.piid = 'All';
    this.country = '0';
    this.state = '0';
    this.params = '';
    if (this.duns && this.duns !== '') {
      if (!this.searchService.countries) {
        this.searchService.getPlaceOfPerformance().subscribe(
          data => {
            this.buildPlaceOfPerformance(data['results']);
          },
          error => (this.error_message = <any>error)
        );
      } else {
        this.countries = this.searchService.countries;
        this.countries.sort(this.searchService.sortByNameAsc);
        this.states = this.searchService.states;
        this.states.sort(this.searchService.sortByCodeAsc);
      }

      this.getContracts(
        this.duns,
        this.current_page,
        this.piid,
        this.naic_code,
        this.country,
        this.state,
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
  buildPlaceOfPerformance(obj: any[]) {
    const countries = [];
    const states = [];
    for (const country of obj) {
      const item = {};
      const state = {};
      item['code'] = country['country_code'];
      item['name'] = country['country_name'];
      if (!this.searchService.existsIn(countries, item['name'], 'name')) {
        countries.push(item);
      }
      if (country['state'] !== null) {
        state['code'] = country['state'];
        if (!this.searchService.existsIn(states, country['state'], 'code')) {
          states.push(state);
        }
      }
    }
    this.countries = countries;
    this.countries.sort(this.searchService.sortByNameAsc);
    this.searchService.countries = this.countries;
    this.states = states;
    this.states.sort(this.searchService.sortByCodeAsc);
    this.searchService.states = this.states;
  }
  getContracts(
    duns: string,
    page: number,
    piid: string,
    naic: string,
    country: string,
    state: string,
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
      .getVendorContractHistory(
        duns,
        page_path,
        piid,
        naic,
        country,
        state,
        ordering
      )
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

        error => {
          this.error_message = <any>error;
          this.spinner = false;
          this.history_no_results = true;
        }
      );
  }
  poolPiids(obj: any[]): string {
    let items = '';
    for (const i of obj) {
      items += i['piid'] + ',';
    }
    return items.slice(0, -1);
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
  setPiid(value: string): string {
    if (value.indexOf('_') !== -1) {
      const arr = value.split('_');
      return (
        '<span class="pull-left">' +
        arr[0] +
        '_</span><span class="pull-left">' +
        arr[1] +
        '</span>'
      );
    } else {
      return value;
    }
  }
  setPoP(obj: any[]): string {
    let pop = '';
    if (obj['country_name']) {
      pop += obj['country_name'];
    }
    if (obj['state'] !== null) {
      pop += ', ' + obj['state'];
    }
    return pop;
  }
  orderBy(ordering: any[]) {
    const order_by = ordering['sort'] + ordering['ordering'];
    this.ordering = ordering['ordering'];
    this.getContracts(
      this.duns,
      1,
      this.piid,
      this.naic_code,
      this.country,
      this.state,
      order_by
    );
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
    if (this.searchService.pools && this.searchService.pools.length > 0) {
      this.naics = this.buildNaicsItems(this.searchService.pools);
      this.naics.sort(this.searchService.sortByCodeAsc);
    } else {
      this.searchService.getNaics(['All']).subscribe(
        data => {
          this.naics = this.buildNaicsItems(data['results']);
          this.naics.sort(this.searchService.sortByCodeAsc);
        },
        error => (this.error_message = <any>error)
      );
    }
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
      this.country,
      this.state,
      this.ordering
    );
  }
  nextPage() {
    this.getContracts(
      this.duns,
      this.next,
      this.piid,
      this.naic_code,
      this.country,
      this.state,
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
        if (prop['piid'] === item) {
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
    if (this.country !== '0') {
      if (params !== '') {
        params += '&';
      }
      params += 'countries=' + this.country;
    }
    if (this.state !== '0') {
      if (params !== '') {
        params += '&';
      }
      params += 'states=' + this.state;
    }
    this.params = params;
  }
  onChangeNaic() {
    this.getContracts(
      this.duns,
      1,
      this.piid,
      this.naic_code,
      this.country,
      this.state,
      this.ordering
    );
    this.setParams();
  }
  onChangeMembership() {
    this.getContracts(
      this.duns,
      1,
      this.piid,
      this.naic_code,
      this.country,
      this.state,
      this.ordering
    );
    this.setParams();
  }
  onChangeCountry() {
    if (this.country !== 'USA') {
      this.state = '0';
    }
    this.getContracts(
      this.duns,
      this.current_page,
      this.piid,
      this.naic_code,
      this.country,
      this.state,
      this.ordering
    );
    this.setParams();
  }
}
