import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment.development';

export interface WeatherResponse {
  location: {
    name: string;
    region: string;
    country: string;
  };
  current: {
    temp_c: number;
    temp_f: number;
    condition: {
      text: string;
      icon: string;
    };
  };
}

@Injectable({
  providedIn: 'root'
})
export class WeatherService {
  private apiUrl = 'http://api.weatherapi.com/v1/current.json';

  constructor(private http: HttpClient) {}

  getWeather(location: string): Observable<WeatherResponse> {
    const params = new HttpParams()
      .set('key', environment.weatherApiKey)
      .set('q', location);

    return this.http.get<WeatherResponse>(this.apiUrl, { params });
  }
}
