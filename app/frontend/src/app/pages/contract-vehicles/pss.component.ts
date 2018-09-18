import { Component, OnInit } from '@angular/core';
import { SearchService } from '../search/search.service';

@Component({
  selector: 'discovery-pss',
  templateUrl: './pss.component.html'
})
export class PssComponent implements OnInit {
  constructor(private searchService: SearchService) {}

  ngOnInit() {}
}
