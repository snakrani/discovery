import { Component, OnInit, Input } from '@angular/core';
declare let document: any;
@Component({
  selector: 'discovery-search-spinner',
  templateUrl: './search-spinner.component.html',
  styleUrls: ['./search-spinner.component.css']
})
export class SearchSpinnerComponent implements OnInit {
  @Input()
  show = true;
  constructor() {}

  ngOnInit() {}
}
