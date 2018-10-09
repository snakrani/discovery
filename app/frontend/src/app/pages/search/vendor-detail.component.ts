import {
  Component,
  OnInit,
  ViewChild,
  Input,
  OnChanges,
  Output,
  EventEmitter
} from '@angular/core';
import { SearchService } from './search.service';
import { ActivatedRoute } from '@angular/router';
import { TblContractHistoryComponent } from './tbl-contract-history.component';

@Component({
  selector: 'discovery-vendor-detail',
  templateUrl: './vendor-detail.component.html',
  styleUrls: ['./vendor-detail.component.css']
})
export class VendorDetailComponent implements OnInit, OnChanges {
  @ViewChild(TblContractHistoryComponent)
  @Input()
  duns: string;
  @Input()
  contract_vehicles;
  @Input()
  service_categories;
  @Input()
  zones;
  @Output()
  emitBack: EventEmitter<boolean> = new EventEmitter();
  @Output()
  emitHideSpinner: EventEmitter<boolean> = new EventEmitter();
  tblContractHistory: TblContractHistoryComponent;
  error_message;
  vendor: any;
  piids_selected: any[] = [];
  spinner = true;
  sbd_col = true;
  more_info = false;
  contract_nums: any[] = [];
  num_show = 3;
  vw_details = true;
  vw_history = false;
  zindex = 30;
  loading = false;
  duns_number;
  constructor(
    private searchService: SearchService,
    private route: ActivatedRoute
  ) {}
  ngOnInit() {}
  ngOnChanges() {
    if (this.duns && this.duns !== '') {
      this.loading = true;
      this.duns_number = this.duns;
      this.getVendorDetails(this.duns);
    }
  }
  backToSearchResults() {
    this.emitBack.emit(true);
  }
  viewDetails() {
    this.vw_details = true;
    this.vw_history = false;
  }
  viewHistory() {
    this.vw_details = false;
    this.vw_history = true;
  }
  onChange(ele) {
    if (ele.getAttribute('aria-expanded') === 'false') {
      ele.innerHTML = 'Less';
    } else {
      ele.innerHTML = 'More';
    }
  }
  getVendorDetails(duns) {
    this.searchService.getVendorDetails(duns).subscribe(
      data => {
        this.vendor = data;
        this.loading = false;
        this.vendor['pools'] = this.buildPoolsByUniqueContractNumber(data);
        this.emitHideSpinner.emit(false);
      },
      error => (this.error_message = <any>error)
    );
  }
  buildItems(obj: any[]) {
    const categories = [];
    for (const category of obj) {
      const item = {};
      item['id'] = category['id'];
      item['name'] = category['name'];
      item['vehicle_id'] = category['vehicle']['id'];
      item['vehicle'] = category['vehicle']['id'].replace('_', ' ');
      categories.push(item);
    }
    return categories;
  }
  getVehicleDescription(vehicle: string) {
    return this.searchService.getItemDescription(
      this.contract_vehicles,
      vehicle,
      'id',
      'name'
    );
  }
  getServiceCategoryDescription(id: string) {
    return this.searchService.getItemDescription(
      this.service_categories,
      id,
      'id',
      'name'
    );
  }

  getContactInfo(contacts: any[]): string {
    let html = '';
    for (const item of contacts) {
      let name = '';
      let phone = '';
      let email = '';
      if (item.name) {
        name = '<strong class="db">' + item.name + '</strong>';
      }
      if (item.phones.length > 0) {
        for (const i of item.phones) {
          phone = '<span class="db">' + i.number + '</span>';
        }
      }
      if (item.emails.length > 0) {
        for (const i of item.emails) {
          email =
            '<span class="db pad-bottom"><a href="mailto:' +
            i.address +
            '">' +
            i.address +
            '</a></span>';
        }
      }
      html += name + phone + email;
    }
    return html;
  }
  getZoneStates(zone: number): string {
    let states = '';
    for (const item of this.zones) {
      if (+item.id === zone) {
        states = this.searchService.commaSeparatedList(item.states, '');
      }
    }
    return states;
  }
  toggleSBD() {
    this.sbd_col = !this.sbd_col;
  }
  toggleMoreInfo() {
    this.more_info = !this.more_info;
  }
  onTop(ele) {
    this.zindex++;
    ele.style.zIndex = this.zindex;
  }
  buildPoolsByUniqueContractNumber(data: any[]) {
    const contracts: any[] = [];
    for (const item of data['pools']) {
      let pool = {};
      if (!this.searchService.existsIn(contracts, item.piid, 'piid')) {
        pool = item;
        pool['service_categories'] = [];
        pool['setasides'] = this.searchService.commaSeparatedList(
          item.setasides,
          'code'
        );
        pool['zones'] = item.zones.sort(this.searchService.sortByIdAsc);
        contracts.push(pool);
      }
      /** Push service categories to contracts */
      for (const cat of contracts) {
        if (cat['piid'] === item.piid) {
          cat['service_categories'].push(item.pool);
        }
      }
    }

    return contracts;
  }
  addItem(num: string) {
    this.piids_selected.push(num);
  }
  removeItem(num: string) {
    for (let i = 0; i < this.piids_selected.length; i++) {
      if (this.piids_selected[i] === num) {
        this.piids_selected.splice(i, 1);
      }
    }
  }
  returnSetAside(arr: any[], code: string): boolean {
    if (arr.length > 0) {
      return arr.includes(code);
    } else {
      return false;
    }
  }
}
