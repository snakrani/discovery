import { Component, OnInit } from '@angular/core';
import { SearchService } from '../search/search.service';

@Component({
  selector: 'discovery-oasis-sb-info',
  templateUrl: './oasis-sb-info.component.html',
  styles: [
    `
      .usa-hero {
        background-image: url(/frontend/assets/images/hero-generic-vehicles.jpg);
        color: #fff !important;
      }
    `
  ]
})
export class OasisSbInfoComponent implements OnInit {
  pools: any[] = [];
  vehicle = 'OASIS_SB';
  error_message;
  constructor(private searchService: SearchService) {}

  ngOnInit() {
    this.searchService.getPoolsByVehicle(this.vehicle).subscribe(
      data => {
        this.pools = data['results'];
      },
      error => (this.error_message = <any>error)
    );
  }
}
