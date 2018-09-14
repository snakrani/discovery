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
  searchKeywords() {
    this.keywords = this.input.nativeElement.value;
    this.searchService.setSearchOptions('keyword', [
      { keyword: this.keywords }
    ]);
    this.router.navigate(['/search'], {
      queryParams: { keywords: this.keywords }
    });
  }
}
