import { Component, OnInit, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'discovery-choose-filters',
  template: `
  <div id="choose-filters" class="text-center tab-pane bordered">

    <span class="icon-arrow-left"></span>
    <h2>Choose your filters and submit your search to begin.</h2>

</div>
  `,
  styles: [
    `
      #choose-filters {
        padding-top: 10%;
        padding-bottom: 10%;
      }
      #choose-filters h2 {
        font-family: 'Source Sans Pro', 'Helvetica Neue', 'Helvetica', 'Roboto',
          'Arial', sans-serif;
        color: #212121 !important;
        font-weight: normal !important;
        padding: 10px;
        width: 50%;
        margin: auto;
      }
    `
  ]
})
export class ChooseFiltersComponent implements OnInit {
  constructor() {}
  ngOnInit() {}
}
