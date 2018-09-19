import { Component, OnInit, ViewChild } from '@angular/core';
import { SearchService } from '../pages/search/search.service';
import { Router } from '@angular/router';
declare let autocomplete: any;
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
  constructor(private searchService: SearchService, private router: Router) {}
  set keywords(value: string) {
    this._keywords = value;
  }
  get keywords(): string {
    return this._keywords;
  }
  ngOnInit() {
    this.searchService.getKeywords().subscribe(data => {
      this.items = data['results'];
      this.keywords_results = this.buildKeywordsDropdown(data['results']);
      autocomplete(this.input.nativeElement, this.keywords_results);
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
        if (this.items[i]['name'] === value) {
          return this.items[i]['id'];
        }
      }
    }
  }
  searchKeywords() {
    this.keywords = this.input.nativeElement.value;
    const keyword_id = this.getItemId(this.keywords);
    if (keyword_id === undefined) {
      console.log('Add note or select first element of autocomplete');
      return;
    }
    this.searchService.setSearchOptions('keyword', [{ keyword: keyword_id }]);
    this.router.navigate(['/search'], {
      queryParams: { keywords: keyword_id }
    });
  }
}
