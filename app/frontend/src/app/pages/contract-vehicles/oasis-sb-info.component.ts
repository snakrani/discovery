import { Component, OnInit } from '@angular/core';
import { SearchService } from '../search/search.service';

@Component({
  selector: 'discovery-oasis-sb-info',
  templateUrl: './oasis-sb-info.component.html'
})
export class OasisSbInfoComponent implements OnInit {
  constructor(private searchService: SearchService) {}

  ngOnInit() {}
}
