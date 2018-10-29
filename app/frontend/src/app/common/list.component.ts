import { Component, OnInit, Input } from '@angular/core';
import { SearchService } from '../pages/search/search.service';

@Component({
  selector: 'discovery-list',
  templateUrl: './list.component.html',
  styles: [
    `
      .cols-2 li {
        float: left;
        width: 49.5% !important;
      }
    `
  ]
})
export class ListComponent implements OnInit {
  @Input()
  id;
  @Input()
  items: any[];
  @Input()
  show_all = false;
  @Input()
  items_to_show = 5;
  @Input()
  key: string;
  @Input()
  columns = '1';
  @Input()
  selected: any[] = [];
  @Input()
  hide_others = false;
  show_more = false;
  title_more = 'Show more';
  constructor(private searchService: SearchService) {}

  ngOnInit() {}
  hideElements() {
    for (let i = 0; i < this.items.length; ++i) {
      if (i > this.items_to_show) {
        document.getElementById('li-' + this.id + '-' + i).style.display =
          'none';
      }
    }
  }
  getValue(item: any) {
    return '<span>' + item[this.key] + '</span>';
  }
  hideOthers(id: string): boolean {
    if (
      this.hide_others &&
      !this.searchService.existsIn(this.selected, id, 'value') &&
      this.selected.length > 0
    ) {
      return true;
    } else {
      return false;
    }
  }
  isSelected(id: string): boolean {
    return this.searchService.existsIn(this.selected, id, 'value');
  }
  showElements() {
    for (let i = 0; i < this.items.length; ++i) {
      if (i >= this.items_to_show) {
        document.getElementById('li-' + this.id + '-' + i).style.display =
          'block';
      }
    }
  }
  toggleMore() {
    this.show_more = !this.show_more;
    if (!this.show_more) {
      this.title_more = 'Show more';
      this.hideElements();
    } else {
      this.title_more = 'Show less';
      this.showElements();
    }
  }
}
