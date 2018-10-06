import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'discovery-list',
  templateUrl: './list.component.html',
  styles: [``]
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

  show_more = false;
  title_more = 'Show more';
  constructor() {}

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
    return item[this.key];
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
