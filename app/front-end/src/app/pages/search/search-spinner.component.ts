import { Component, OnInit, Input, OnChanges } from '@angular/core';
declare let document: any;
@Component({
  selector: 'discovery-search-spinner',
  templateUrl: './search-spinner.component.html',
  styleUrls: ['./search-spinner.component.css']
})
export class SearchSpinnerComponent implements OnInit, OnChanges {
  @Input()
  show = true;
  constructor() {}

  ngOnInit() {}
  ngOnChanges() {}
}
