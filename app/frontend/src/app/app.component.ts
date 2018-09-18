import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'discovery-root',
  templateUrl: './app.component.html',
  styles: [``]
})
export class AppComponent {
  title = 'discovery';
  another: string;
  constructor(private route: ActivatedRoute) {}
}
