import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SearchComponent } from './search.component';
import { FiltersComponent } from './filters.component';
import { ActiveFiltersComponent } from './filters/active-filters.component';
import { FilterContractVehiclesComponent } from './filters/filter-contract-vehicles.component';
import { FilterSbdComponent } from './filters/filter-sbd.component';
import { ChooseFiltersComponent } from './choose-filters.component';
import { FilterKeywordsComponent } from './filters/filter-keywords.component';
import { FormsModule } from '@angular/forms';
import { ModalComponent } from '../../common/modal.component';
import { SpinnerComponent } from '../../common/spinner.component';
import { FilterNaicsComponent } from './filters/filter-naics.component';
import { FilterServiceCategoriesComponent } from './filters/filter-service-categories.component';
import { FilterCertificationsComponent } from './filters/filter-certifications.component';
import { FilterContractPricingTypeComponent } from './filters/filter-contract-pricing-type.component';
import { FilterContractObligatedAmountComponent } from './filters/filter-contract-obligated-amount.component';
import { FilterAgencyPerformanceComponent } from './filters/filter-agency-performance.component';
import { FilterPscComponent } from './filters/filter-psc.component';
import { FilterZoneComponent } from './filters/filter-zone.component';
import { ListComponent } from '../../common/list.component';
import { VendorDetailComponent } from './vendor-detail.component';
import { TblContractHistoryComponent } from './tbl-contract-history.component';
import { SearchSpinnerComponent } from './search-spinner.component';
import { ThSortComponent } from './th-sort.component';
import { TblVendorsComponent } from './tbl-vendors.component';
import { LnkToggleHeightsComponent } from './lnk-toggle-heights.component';
import { FilterSelectedComponent } from './filters/filter-selected.component';
import { AutocompleteComponent } from './filters/autocomplete.component';
import { FilterPlaceOfPerformanceComponent } from './filters/filter-place-of-performance.component';

@NgModule({
  imports: [CommonModule, FormsModule],
  declarations: [
    SearchComponent,
    ModalComponent,
    FiltersComponent,
    ActiveFiltersComponent,
    ChooseFiltersComponent,
    FilterKeywordsComponent,
    FilterContractVehiclesComponent,
    FilterSbdComponent,
    FilterNaicsComponent,
    FilterServiceCategoriesComponent,
    FilterCertificationsComponent,
    FilterContractPricingTypeComponent,
    FilterContractObligatedAmountComponent,
    FilterAgencyPerformanceComponent,
    FilterPscComponent,
    FilterZoneComponent,
    FilterPlaceOfPerformanceComponent,
    SpinnerComponent,
    ListComponent,
    VendorDetailComponent,
    SearchSpinnerComponent,
    TblContractHistoryComponent,
    TblVendorsComponent,
    ThSortComponent,
    LnkToggleHeightsComponent,
    FilterSelectedComponent,
    AutocompleteComponent
  ]
})
export class SearchModule {}
