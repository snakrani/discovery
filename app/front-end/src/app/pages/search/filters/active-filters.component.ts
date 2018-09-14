import { Component, OnInit, Input, OnChanges } from '@angular/core';
import { SearchService } from '../search.service';
import { ActivatedRoute } from '@angular/router';
@Component({
  selector: 'discovery-active-filters',
  templateUrl: './active-filters.component.html',
  styles: [
    `
      .usa-accordion-button,
      .usa-accordion > li {
        background-color: transparent !important;
        border-top: 0px !important;
      }
      .usa-accordion .usa-accordion-button[aria-expanded='true'] {
        border-left-color: transparent !important;
        color: #212121;
      }
      .ul-filters li {
        border: 1px solid #b7b7b7;
        list-style: none;
        padding: 4px 10px;
        border-radius: 2px;
        float: left;
        margin-right: 4px;
      }
      .ul-filters {
        clear: both;
        margin: 0px;
        padding: 0px;
      }
      .usa-accordion-content {
        border-bottom: 1px solid #5b616b;
        padding-top: 0px;
      }
    `
  ]
})
export class ActiveFiltersComponent implements OnInit, OnChanges {
  @Input()
  filters: any[] = [];
  constructor(
    private searchService: SearchService,
    private route: ActivatedRoute
  ) {
    const filt = this.searchService.activeFilters;
  }

  ngOnInit() {}
  ngOnChanges() {}
  clear() {
    this.filters = [];
  }
  setFilters(filters) {
    this.filters = filters;
  }
}
