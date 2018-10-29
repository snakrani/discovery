import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'discovery-lnk-toggle-heights',
  template: `<button id="btn-{{toggle_id}}"
  (click)="toggleMore()" class="button-link-more db" [class.less]="opened" [attr.aria-expanded]="opened">
  {{title_more}}
</button>
`,
  styles: [
    `
      .button-link-more {
        background-color: transparent !important;
        background-position: right 0.8em center;
        background-image: url(/frontend/assets/uswds/img/angle-arrow-down-primary.png) !important;
        background-image: url(/frontend/assets/uswds/img/angle-arrow-down-primary.svg) !important;
        padding: 1rem 4rem 1rem 0 !important;
        background-size: 1.1rem !important;
        background-repeat: no-repeat;
        width: auto;
        min-width: 90px;
        color: #0071bc;
        font-weight: normal;
      }
      .button-link-more.less {
        background-image: url(/frontend/assets/uswds/img/angle-arrow-up-primary.png) !important;
        background-image: url(/frontend/assets/uswds/img/angle-arrow-up-primary.svg);
      }
    `
  ]
})
export class LnkToggleHeightsComponent implements OnInit {
  @Input()
  toggle_id;
  @Input()
  label: string;
  @Output()
  emitToggleId: EventEmitter<string> = new EventEmitter();
  opened = false;

  show_more = false;
  title_more = 'More';
  constructor() {}

  ngOnInit() {}
  toggleMore() {
    this.show_more = !this.show_more;
    if (!this.show_more) {
      this.title_more = 'More';
      this.opened = false;
    } else {
      this.title_more = 'Less';
      this.opened = true;
    }
    this.emitToggleId.emit(this.toggle_id);
  }
}
