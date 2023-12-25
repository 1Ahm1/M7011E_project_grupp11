import { Component, inject } from '@angular/core';
import { UserProfile } from '../interfaces/entities';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html'
})
export class ProfileComponent {
  
  private authService: AuthService = inject(AuthService);
  profile: UserProfile = {
    userId: 0,
    email: '',
    phoneNumber: '',
    defaultLang: '',
    defaultRole: '',
    name: '',
    imageUrl: ''
  }

  constructor() {
    
  }

  ngOnInit() {
    this.getProfile();
  }

  async getProfile() {
    try
    {
      this.profile = await this.authService.getProfile(); 
    }
    catch(e) {
      console.log('error fetching profile');
    }
  }

  async updateProfile() {
    try
    {
      await this.authService.updateProfile(this.profile.name); 
    }
    catch(e) {
      console.log('error updating profile');
    }
  }
}
