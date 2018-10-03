import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'discovery-contracts',
  templateUrl: './contracts.component.html',
  styles: [
    `
      .usa-hero {
        background-image: url(/frontend/assets/images/hero-resources.jpg);
        color: #fff !important;
      }
      .circle {
        background: #2d71b6;
        color: #fff;
        padding: 15px 10px;
        text-align: center;
        display: table-cell;
        vertical-align: middle;
        width: 120px;
        height: 120px;
        float: left;
        border-radius: 10em;
        margin-right: 25px;
      }
      .circle h3 {
        color: #fff;
      }
    `
  ]
})
export class ContractsComponent implements OnInit {
  constructor() {}

  ngOnInit() {}
}
