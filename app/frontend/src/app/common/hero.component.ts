import { Component, OnInit, ViewChild } from '@angular/core';
import { SearchService } from '../pages/search/search.service';
import { Router } from '@angular/router';
declare let autocomplete: any;
declare const $: any;
declare let document: any;
@Component({
  selector: 'discovery-hero',
  templateUrl: './hero.component.html',
  styleUrls: ['./hero.component.css']
})
export class HeroComponent implements OnInit {
  items: any[] = [];
  _keywords = '';
  keywords_results: any[] = [];
  keywords_input;
  @ViewChild('keywordInput')
  input;
  naics;
  pscs;
  loading = true;
  server_error = false;
  error_message;
  _option = 'naic';
  constructor(private searchService: SearchService, private router: Router) {}
  set option(value: string) {
    this._option = value;
    this.setInputData(value);
  }
  get option(): string {
    return this._option;
  }
  set keywords(value: string) {
    this._keywords = value;
  }
  get keywords(): string {
    return this._keywords;
  }
  ngOnInit() {
    this.loading = true;
    this.searchService.getKeywords().subscribe(data => {
      this.items = data['results'];
      this.keywords_results = this.buildKeywordsDropdown(data['results']);
      this.searchService.keywords = this.keywords_results;
      this.initPools();
    });
  }
  setInputData(value: string) {
    switch (value) {
      case 'keyword':
        this.setKeywordAutoComplete(this.keywords_results);
        break;
      case 'naic':
        this.setKeywordAutoComplete(this.naics);
        break;
      case 'psc':
        this.setKeywordAutoComplete(this.pscs);
        break;
    }
  }
  initPools() {
    this.searchService.getPools(['All']).subscribe(
      data => {
        this.searchService.pools = data['results'];
        this.buildNaicsItems(this.searchService.pools);
        this.buildPscsItems(this.searchService.pools);
        this.option = 'naic';
        this.loading = false;
      },
      error => {
        this.server_error = true;
        this.error_message = <any>error;
      }
    );
  }
  onChange() {}
  buildNaicsItems(obj: any[]) {
    const naics = [];
    for (const pool of obj) {
      for (const naic of pool.naics) {
        const item = {};
        item['code'] = naic.code;
        item['name'] = naic.code + ' - ' + naic.description;
        if (!this.searchService.existsIn(naics, naic.code, 'code')) {
          naics.push(item);
        }
      }
    }
    this.naics = naics;
    this.naics.sort(this.searchService.sortByCodeAsc);
  }
  buildPscsItems(obj: any[]) {
    const naics = [];
    const pscs = [];
    for (const pool of obj) {
      for (const psc of pool.psc) {
        const item = {};
        item['code'] = psc.code;
        item['name'] = psc.code + ' - ' + psc.description;
        if (!this.searchService.existsIn(pscs, psc.code, 'code')) {
          pscs.push(item);
        }
      }
    }
    this.pscs = pscs;
    this.pscs.sort(this.searchService.sortByCodeAsc);
  }
  setKeywordAutoComplete(data) {
    $('#keyword, #hero-keywords-input').val('');
    const options = {
      data: data,
      theme: 'square',
      getValue: 'name',
      list: {
        maxNumberOfElements: 100,
        match: {
          enabled: true
        },
        onSelectItemEvent: function() {
          $('#keyword').val(
            $('#hero-keywords-input').getSelectedItemData().code
          );
          $('#error-msg').addClass('hide');
          $('#hero-keywords-input').removeClass('input-error');
        }
      }
    };
    $('#hero-keywords-input').easyAutocomplete(options);
  }
  buildKeywordsDropdown(obj: any[]): any[] {
    const keywords = [];
    for (const item of obj) {
      const keyword = {};
      keyword['name'] = item['name'];
      keyword['code'] = item['id'];
      keywords.push(keyword);
    }
    return keywords;
  }
  getItemId(value: string): string {
    if (value) {
      for (let i = 0; i < this.items.length; i++) {
        if (this.items[i]['name'] === value) {
          return this.items[i]['id'];
        }
      }
    }
  }
  searchKeywords() {
    const keyword_id = $('#keyword').val();
    if (keyword_id === '') {
      $('#error-msg').removeClass('hide');
      $('#hero-keywords-input').addClass('input-error');
      return;
    }
    switch (this.option) {
      case 'keyword':
        this.searchService.setSearchOptions('keyword', [
          { keyword: keyword_id }
        ]);
        this.router.navigate(['/search'], {
          queryParams: { keywords: keyword_id }
        });
        break;
      case 'naic':
        this.searchService.setSearchOptions('naics', [{ naics: keyword_id }]);
        this.router.navigate(['/search'], {
          queryParams: { naics: keyword_id }
        });
        break;
      case 'psc':
        this.searchService.setSearchOptions('pscs', [{ pscs: keyword_id }]);
        this.router.navigate(['/search'], {
          queryParams: { pscs: keyword_id }
        });
        break;
    }
  }
}
