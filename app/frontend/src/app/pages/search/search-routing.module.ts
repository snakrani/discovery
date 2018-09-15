import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { SearchComponent } from './search.component';
import { ChooseFiltersComponent } from './choose-filters.component';

const routes: Routes = [
  {
    path: 'search',
    component: SearchComponent
  }
];
// const routes: Routes = [
//   {
//     path: 'search',
//     component: SearchComponent,
//     children: [
//       { path: '', component: ChooseFiltersComponent },
//       { path: 'contracts/:search', component: ContractsComponent },
//       { path: 'contracts', redirectTo: '/search', pathMatch: 'full' },
//       { path: 'vendors/:search', component: VendorsComponent },
//       { path: 'vendors', redirectTo: '/search', pathMatch: 'full' }
//     ]
//   }
// ];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class SearchRoutingModule {}
