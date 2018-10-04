import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'discovery-lnk-toggle-heights',
  template: `<button (click)="toggleMore()" class="usa-accordion-button usa-accordion-button-as-link db" [attr.aria-expanded]="opened">
  {{title_more}}
</button>
`,
  styles: [``]
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
