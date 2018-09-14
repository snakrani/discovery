import { Component, OnInit, Input, OnDestroy, ElementRef } from '@angular/core';
import { ModalService } from './modal.service';

@Component({
  selector: 'discovery-modal',
  template: `
  <div class="modal">
      <div id="modal-content" class="modal-content">
          <a class="close" (click)="close()">&times;</a>
          <h3>{{title}}</h3>
          <div class="modal-inner"> <ng-content></ng-content></div>
      </div>
  </div>
  <div class="modal-background"></div>
  `
})
export class ModalComponent implements OnInit, OnDestroy {
  @Input()
  id: string;
  @Input()
  title: string;
  private element: any;

  constructor(private modalService: ModalService, private el: ElementRef) {
    this.element = el.nativeElement;
  }

  ngOnInit(): void {
    const modal = this;

    // ensure id attribute exists
    if (!this.id) {
      console.error('modal must have an id');
      return;
    }

    // move element to bottom of page (just before </body>) so it can be displayed above everything else
    document.body.appendChild(this.element);

    // close modal on background click
    this.element.addEventListener('click', function(e: any) {
      if (e.target.className === 'modal') {
        modal.close();
      }
    });

    // add self (this modal instance) to the modal service so it's accessible from controllers
    this.modalService.add(this);
  }

  // remove self from modal service when directive is destroyed
  ngOnDestroy(): void {
    this.modalService.remove(this.id);
    this.element.remove();
  }

  // open modal
  open(): void {
    this.element.className = 'show';
    document.body.classList.add('modal-open');
  }

  // close modal
  close(): void {
    this.element.classList.remove('show');
    document.body.classList.remove('modal-open');
  }
}
