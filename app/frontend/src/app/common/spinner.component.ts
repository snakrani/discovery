import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'discovery-spinner',
  template: `
    <div class="spinner">
      <img src="{{APP_ASSETS}}assets/images/loader.gif" alt="Loading" class="pull-left" /><strong class="pull-left">Loading</strong>
    </div>
  `,
  styles: []
})
export class SpinnerComponent implements OnInit {
  @Input()
  show = true;
  APP_ASSETS = '/frontend/';

  constructor() {}

  ngOnInit() {}
}
