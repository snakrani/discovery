import {
  Component,
  OnInit,
  Input,
  Output,
  EventEmitter,
  OnChanges
} from '@angular/core';
declare const $: any;
@Component({
  selector: 'discovery-autocomplete',
  templateUrl: './autocomplete.component.html',
  styles: []
})
export class AutocompleteComponent implements OnChanges {
  @Input()
  id: string;
  @Input()
  keywords_results: any[];
  @Input()
  placeholder: string;
  @Output()
  emitCode: EventEmitter<string> = new EventEmitter();
  keywords = '';
  constructor() {}
  ngOnChanges() {
    if (this.keywords_results && this.keywords_results.length > 0) {
      this.setKeywordAutoComplete(this.keywords_results, this.id);
    }
  }
  addKeywords() {
    const code = $('#' + this.id + '-value').val();
    this.emitCode.emit(code);
    $('#' + this.id + '-input').val('');
  }
  setKeywordAutoComplete(data, id) {
    $('#' + id + '-value, #' + id + '-input').val('');
    const options = {
      data: data,
      theme: 'square',
      getValue: 'name',
      list: {
        maxNumberOfElements: 100,
        match: {
          enabled: true
        },
        onSelectItemEvent: function() {
          $('#' + id + '-value').val(
            $('#' + id + '-input').getSelectedItemData().code
          );
          // $('#error-msg').addClass('hide');
          $('#' + id + '-input').removeClass('input-error');
        },
        onHideListEvent: function() {
          if ($('#' + id + '-value').val() === '') {
            $('#' + id + '-input').val('');
          }
        }
      }
    };
    $('#' + this.id + '-input').easyAutocomplete(options);
  }
}
