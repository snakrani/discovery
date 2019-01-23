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
    <a (click)="order()" [class]="orderClass" [style.minWidth]="width">{{label}}</a>
  `,
  styles: [
    `
      a {
        text-decoration: none;
        display: block;
        padding-right: 25px;
        background-image: url(/frontend/assets/images/icon-sort-default.png);
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
export class ThSortComponent {
  @Input()
  label: string;
  @Input()
  table: any;
  @Input()
  orderBy: string;
  @Input()
  width = '90px';
  @Output()
  emmitOrdering: EventEmitter<any> = new EventEmitter();
  orderClass = '';
  constructor() {}
 
  order() {
    if (this.table.orderBy !== this.orderBy) {
      this.table.sortBy = 'asc';
    }
    switch (this.table.sortBy) {
      case 'asc':
        this.orderClass = 'desc';
        this.table.sortBy = 'desc'
        this.emmitOrdering.emit({ ordering: this.orderBy, sort: '' });
        break;
      case 'desc':
        this.orderClass = 'asc';
        this.table.sortBy = 'asc'
        this.emmitOrdering.emit({ ordering: this.orderBy, sort: '-' });
        break;
    }
  }
}
