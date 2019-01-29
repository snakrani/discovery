import { Component, OnInit } from '@angular/core';
import { SearchService } from '../search/search.service';

@Component({
  selector: 'discovery-hcats',
  templateUrl: './hcats.component.html',
  styles: [
    `
      .usa-hero {
        background-image: url(/frontend/assets/images/hero-generic-vehicles.jpg);
        color: #fff !important;
      }
    `
  ]
})
export class HcatsComponent implements OnInit {
  pools: any[] = [];
  vehicle = 'HCATS';
  error_message;
  constructor(private searchService: SearchService) {}

  ngOnInit() {
    this.searchService.getPoolsByVehicle(this.vehicle).subscribe(
      data => {
        this.pools = data['results'];
        this.pools.sort(this.searchService.sortByNumberAsc);
      },
      error => (this.error_message = <any>error)
    );
  }
}
