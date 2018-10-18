import { Component, Input } from '@angular/core';
declare const $: any;
@Component({
  selector: 'discovery-filter-selected',
  template: `
  <div [id]="id" class="hide" *ngIf="id">
  <p>
  <strong class="db">{{label}}.</strong>
  Please submit to see results.</p>
</div>`,
  styles: [
    `
      div {
        background-image: url(/frontend/assets/images/success.png);
        background-image: url(/frontend/assets/images/success.svg);
        background-repeat: no-repeat;
        background-size: 40px auto;
        padding-left: 40px;
      }
      p {
        color: #488248;
      }
    `
  ]
})
export class FilterSelectedComponent {
  @Input()
  id: string;
  @Input()
  label: string;

  constructor() {}
  showMsg() {
    $('#' + this.id).fadeIn(1000, function() {
      $(this).fadeOut(1000);
    });
  }
}
