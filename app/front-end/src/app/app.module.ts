import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HttpClientModule } from '@angular/common/http';
import { AboutComponent } from './pages/about/about.component';
import { ResourcesComponent } from './pages/resources/resources.component';
import { OasisSbInfoComponent } from './pages/contract-vehicles/oasis-sb-info.component';
import { HelpComponent } from './pages/help/help.component';
import { BmoInfoComponent } from './pages/contract-vehicles/bmo-info.component';
import { HcatsComponent } from './pages/contract-vehicles/hcats.component';
import { PssComponent } from './pages/contract-vehicles/pss.component';
import { HeroComponent } from './common/hero.component';
import { WelcomeComponent } from './pages/welcome/welcome.component';
import { Error404Component } from './pages/error404/error404.component';
import { SearchModule } from './pages/search/search.module';

@NgModule({
  declarations: [
    AppComponent,
    HeroComponent,
    WelcomeComponent,
    Error404Component,
    AboutComponent,
    ResourcesComponent,
    OasisSbInfoComponent,
    HelpComponent,
    BmoInfoComponent,
    HcatsComponent,
    PssComponent,
    HeroComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpClientModule,
    SearchModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {}
