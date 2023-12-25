import { Component, inject } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-activate-user',
  templateUrl: './activate-user.component.html',
  styleUrls: ['./activate-user.component.css']
})
export class ActivateUserComponent {

  constructor(private router: Router) {}
  validationCode: number | undefined;
  codeError:boolean = false;
  private authService: AuthService = inject(AuthService);

  async validateUser(){
    try
    {
      if(typeof this.validationCode !== 'undefined')
      {
        const data = await this.authService.validateUser(Number(this.validationCode!))
        this.validationCode = 0;
        this.codeError = false;
        if(data.userProfile.defaultRole == 'customer')
          this.router.navigate(['home/']);
        else
          this.router.navigate(['manager/home/']);
      }
    }
    catch(e) {
      this.codeError = true;
    }
  }
}
