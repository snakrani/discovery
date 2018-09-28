import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'discovery-lnk-toggle-heights',
  template: `<a class="db pad-top" (click)="toggleMore()">{{title_more}} {{label}}</a>
`,
  styles: [
    `
      a {
        font-weight: normal;
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

  show_more = false;
  title_more = 'Show all';
  constructor() {}

  ngOnInit() {}

  toggleMore() {
    this.show_more = !this.show_more;
    if (!this.show_more) {
      this.title_more = 'Show all';
    } else {
      this.title_more = 'Show less';
    }
    this.emitToggleId.emit(this.toggle_id);
  }
}
