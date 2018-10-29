import { Component, OnInit, ViewChild, Input } from '@angular/core';
import { SearchService } from '../pages/search/search.service';
import { Router } from '@angular/router';
import { ThSortComponent } from '../pages/search/th-sort.component';
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
  placeholder = '';
  interval;
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
    if (this.searchService.keywords && this.searchService.keywords.length) {
      this.buildKeywordsDropdown(this.searchService.keywords);
      this.buildNaicsItems(this.searchService.pools);
      this.buildPscsItems(this.searchService.pools);
      this.loading = false;
      this.option = 'naic';
    } else {
      this.loading = true;
      this.searchService.getKeywords().subscribe(data => {
        this.searchService.keywords = this.keywords_results;
        this.buildKeywordsDropdown(data['results']);

        this.initPools();
      });
    }
  }
  onChange() {}
  setInputData(value: string) {
    if (value === 'keyword') {
      this.items = this.keywords_results;
    } else if (value === 'naic') {
      this.items = this.naics;
    } else if (value === 'psc') {
      this.items = this.pscs;
    }
    this.setKeywordAutoComplete(this.items);
  }
  setKeywordAutoComplete(data) {
    $('#keyword')
      .children('option:not(:first)')
      .remove();
    $('#keyword').select2({
      data: data,
      selectOnClose: true
    });
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

  buildNaicsItems(obj: any[]) {
    const results = [];
    for (const pool of obj) {
      for (const naic of pool.naics) {
        const item = {};
        item['id'] = naic.code;
        item['text'] = naic.code + ' - ' + naic.description;
        item['pool_id'] = pool.id;
        if (!this.searchService.existsIn(results, naic.code, 'id')) {
          results.push(item);
        }
      }
    }
    this.naics = results;
    this.naics.sort(this.searchService.sortByIdAsc);
  }
  buildPscsItems(obj: any[]) {
    const results = [];
    for (const pool of obj) {
      for (const psc of pool.psc) {
        const item = {};
        item['id'] = psc.code;
        item['text'] = psc.code + ' - ' + psc.description;
        item['pool_id'] = pool.id;
        if (!this.searchService.existsIn(results, psc.code, 'id')) {
          results.push(item);
        }
      }
    }
    this.pscs = results;
    this.pscs.sort(this.searchService.sortByIdAsc);
  }

  buildKeywordsDropdown(obj: any[]) {
    const keywords = [];
    for (const item of obj) {
      const keyword = {};
      keyword['text'] = item['name'];
      keyword['id'] = item['id'];
      keywords.push(keyword);
    }
    this.keywords_results = keywords;
    // this.keywords_results.sort(this.searchService.sortByTextAsc);
  }

  searchKeywords() {
    const keyword_id = $('#keyword').val();
    // return;
    if (keyword_id === '0') {
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
