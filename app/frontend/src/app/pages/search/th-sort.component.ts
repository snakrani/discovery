import {
  Component,
  Input,
  Output,
  EventEmitter,
  OnChanges
} from '@angular/core';

@Component({
  selector: 'discovery-th-sort',
  template: `
    <a (click)="order()" [class]="orderClass">{{label}}</a>
  `,
  styles: [
    `
      a {
        min-width: 120px;
        text-decoration: none;
        display: block;
        padding-right: 25px;
        background-image: url(/frontend/assets/images/icon-sort-default.png);
        background-image: url(/frontend/assets/images/icon-sort-default.svg);
        background-repeat: no-repeat;
        background-size: auto 20px;
        background-position: right center;
      }
      a.asc {
        background-image: url(/frontend/assets/images/icon-sort-asc.png);
        background-image: url(/frontend/assets/images/icon-sort-asc.svg);
      }
      a.desc {
        background-image: url(/frontend/assets/images/icon-sort-desc.png);
        background-image: url(/frontend/assets/images/icon-sort-desc.svg);
      }
    `
  ]
})
export class ThSortComponent implements OnChanges {
  @Input()
  label: string;
  @Input()
  selectedParentOrdering: string;
  @Input()
  ordering: string;
  @Output()
  emmitOrdering: EventEmitter<any> = new EventEmitter();
  orderClass = '';
  constructor() {}
  ngOnChanges() {
    if (this.selectedParentOrdering !== this.ordering) {
      this.reset();
    }
  }
  order(ele) {
    switch (this.orderClass) {
      case '':
        this.orderClass = 'asc';
        this.emmitOrdering.emit({ ordering: this.ordering, sort: '' });
        break;
      case 'asc':
        this.orderClass = 'desc';
        this.emmitOrdering.emit({ ordering: this.ordering, sort: '-' });
        break;
      case 'desc':
        this.orderClass = 'asc';
        this.emmitOrdering.emit({ ordering: this.ordering, sort: '' });
        break;
    }
  }
  reset() {
    this.orderClass = '';
  }
}
