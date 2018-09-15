import { Component, OnInit } from '@angular/core';
import { SearchService } from '../search/search.service';
// declare let $: any;
@Component({
  templateUrl: './about.component.html',
  styleUrls: ['./about.component.css']
})
export class AboutComponent implements OnInit {
  constructor(private searchService: SearchService) {}

  ngOnInit() {}
}
