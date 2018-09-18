import { Component, OnInit } from '@angular/core';
import { SearchService } from '../search/search.service';

@Component({
  selector: 'discovery-bmo-info',
  templateUrl: './bmo-info.component.html'
})
export class BmoInfoComponent implements OnInit {
  constructor(private searchService: SearchService) {}

  ngOnInit() {}
}
