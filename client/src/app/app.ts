import { Component, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { WeatherService } from './Services/weather.service';

@Component({
  selector: 'app-root',
  imports: [FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  location: string = '';
  loading = signal(false);
  locationName = signal('');
  temperature = signal<number | null>(null);
  error = signal<string>('');

  constructor(private weatherService: WeatherService) {}

  searchWeather(): void {
    if (!this.location.trim()) {
      this.error.set('Please enter a location');
      return;
    }

    this.loading.set(true);
    this.error.set('');
    this.locationName.set('');
    this.temperature.set(null);

    this.weatherService.getWeather(this.location).subscribe({
      next: (response) => {
        this.locationName.set(response.location.name);
        this.temperature.set(response.current.temp_c);
        this.loading.set(false);
      },
      error: (err) => {
        this.loading.set(false);
        if (err.error?.error?.message) {
          this.error.set(err.error.error.message);
        } else {
          this.error.set('Failed to fetch weather data. Please try again.');
        }
      }
    });
  }
}
