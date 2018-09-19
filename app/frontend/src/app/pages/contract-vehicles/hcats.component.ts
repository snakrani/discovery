import { Component, OnInit } from '@angular/core';
import { SearchService } from '../search/search.service';

@Component({
  selector: 'discovery-hcats',
  templateUrl: './hcats.component.html'
})
export class HcatsComponent implements OnInit {
  constructor(private searchService: SearchService) {}

  ngOnInit() {}
}
